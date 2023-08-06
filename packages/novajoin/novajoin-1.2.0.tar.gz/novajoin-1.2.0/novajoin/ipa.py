# Copyright 2016 Red Hat, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import cachetools
import json
import os
import time
import uuid

import six
from six.moves import http_client


try:
    from gssapi.exceptions import GSSError
    from ipalib import api
    from ipalib import errors
    ipalib_imported = True
except ImportError:
    # ipalib/ipapython are not available in PyPy yet, don't make it
    # a showstopper for the tests.
    ipalib_imported = False

if ipalib_imported:
    try:
        from ipapython.ipautil import kinit_keytab
    except ImportError:
        # The import moved in freeIPA 4.5.0
        try:
            from ipalib.install.kinit import kinit_keytab
        except ImportError:
            ipalib_imported = False

from novajoin import exception
from novajoin.util import get_domain
from oslo_config import cfg
from oslo_log import log as logging
from six.moves.configparser import SafeConfigParser


CONF = cfg.CONF

LOG = logging.getLogger(__name__)


class IPANovaJoinBase(object):

    def __init__(self):
        if not ipalib_imported:
            return

        self.ntries = CONF.connect_retries
        self.initial_backoff = CONF.connect_backoff
        self.ccache = "MEMORY:" + str(uuid.uuid4())
        LOG.debug("cache: %s", self.ccache)
        os.environ['KRB5CCNAME'] = self.ccache
        if self._ipa_client_configured() and not api.isdone('finalize'):
            (hostname, realm) = self.get_host_and_realm()
            kinit_keytab(str('nova/%s@%s' % (hostname, realm)),
                         CONF.keytab, self.ccache)
            api.bootstrap(context='novajoin')
            api.finalize()
        self.batch_args = list()
        self.backoff = self.initial_backoff

    def split_principal(self, principal):
        """Split a principal into its components. Copied from IPA 4.0.0"""
        service = hostname = realm = None

        # Break down the principal into its component parts, which may or
        # may not include the realm.
        sp = principal.split('/')
        if len(sp) != 2:
            raise errors.MalformedServicePrincipal(reason=_('missing service'))

        service = sp[0]
        if len(service) == 0:
            raise errors.MalformedServicePrincipal(reason=_('blank service'))
        sr = sp[1].split('@')
        if len(sr) > 2:
            raise errors.MalformedServicePrincipal(
                reason=_('unable to determine realm'))

        hostname = sr[0].lower()
        if len(sr) == 2:
            realm = sr[1].upper()
            # At some point we'll support multiple realms
            if realm != api.env.realm:
                raise errors.RealmMismatch()
        else:
            realm = api.env.realm

        # Note that realm may be None.
        return (service, hostname, realm)

    def split_hostname(self, hostname):
        """Split a hostname into its host and domain parts"""
        parts = hostname.split('.')
        domain = six.text_type('.'.join(parts[1:]) + '.')
        return (parts[0], domain)

    def get_host_and_realm(self):
        """Return the hostname and IPA realm name.

           IPA 4.4 introduced the requirement that the schema be
           fetched when calling finalize(). This is really only used by
           the ipa command-line tool but for now it is baked in.
           So we have to get a TGT first but need the hostname and
           realm. For now directly read the IPA config file which is
           in INI format and pull those two values out and return as
           a tuple.
        """
        config = SafeConfigParser()
        config.read('/etc/ipa/default.conf')
        hostname = config.get('global', 'host')
        realm = config.get('global', 'realm')

        return (hostname, realm)

    def __backoff(self, message_id):
        LOG.debug("[%s] Backing off %s seconds", message_id, self.backoff)
        time.sleep(self.backoff)
        if self.backoff < 512:
            self.backoff = self.backoff * 2

    def __reset_backoff(self, message_id):
        if self.backoff > self.initial_backoff:
            LOG.debug("[%s] Resetting backoff to %d",
                      message_id, self.initial_backoff)
            self.backoff = self.initial_backoff

    def __get_connection(self, message_id):
        """Make a connection to IPA or raise an error."""
        tries = 0

        while (tries <= self.ntries):
            LOG.debug("[%s] Attempt %d of %d", message_id, tries, self.ntries)
            if api.Backend.rpcclient.isconnected():
                api.Backend.rpcclient.disconnect()
            try:
                api.Backend.rpcclient.connect()
                # ping to force an actual connection in case there is only one
                # IPA master
                api.Command[u'ping']()
            except (errors.CCacheError,
                    errors.TicketExpired,
                    errors.KerberosError) as e:
                tries += 1
                LOG.debug("[%s] kinit again: %s", message_id, e)
                # pylint: disable=no-member
                try:
                    kinit_keytab(str('nova/%s@%s' %
                                 (api.env.host, api.env.realm)),
                                 CONF.keytab,
                                 self.ccache)
                except GSSError as e:
                    LOG.debug("[%s] kinit failed: %s", message_id, e)
                    if self.backoff:
                        self.__backoff(message_id)
            except errors.NetworkError:
                tries += 1
                if self.backoff:
                    self.__backoff(message_id)
            except http_client.ResponseNotReady:
                # NOTE(xek): This means that the server closed the socket,
                # so keep-alive ended and we can't use that connection.
                api.Backend.rpcclient.disconnect()
                tries += 1
                if self.backoff:
                    self.__backoff(message_id)
            else:
                # successful connection
                self.__reset_backoff(message_id)
                return

        LOG.error("[%s] Failed to connect to IPA after %d attempts",
                  message_id, self.ntries)
        raise exception.IPAConnectionError(tries=self.ntries)

    def start_batch_operation(self, message_id=0):
        """Start a batch operation.

           IPA method calls will be collected in a batch job
           and submitted to IPA once all the operations have collected
           by a call to _flush_batch_operation().
        """
        LOG.debug("[%s] start batch operation", message_id)
        self.batch_args = list()

    def _add_batch_operation(self, command, *args, **kw):
        """Add an IPA call to the batch operation"""
        self.batch_args.append({
            "method": six.text_type(command),
            "params": [args, kw],
        })

    def flush_batch_operation(self, message_id=0):
        """Make an IPA batch call."""
        LOG.debug("[%s] flush_batch_operation", message_id)
        if not self.batch_args:
            return None

        kw = {}
        LOG.debug("[%s] %s", message_id, self.batch_args)

        return self._call_ipa(message_id, 'batch', *self.batch_args, **kw)

    def _call_ipa(self, message_id, command, *args, **kw):
        """Make an IPA call."""
        if not api.Backend.rpcclient.isconnected():
            self.__get_connection(message_id)
        if 'version' not in kw:
            kw['version'] = u'2.146'  # IPA v4.2.0 for compatibility

        while True:
            try:
                result = api.Command[command](*args, **kw)
                LOG.debug(result)
                return result
            except (errors.CCacheError,
                    errors.TicketExpired,
                    errors.KerberosError):
                LOG.debug("[%s] Refresh authentication", message_id)
                self.__get_connection(message_id)
            except errors.NetworkError:
                if self.backoff:
                    self.__backoff(message_id)
                else:
                    raise
            except http_client.ResponseNotReady:
                # NOTE(xek): This means that the server closed the socket,
                # so keep-alive ended and we can't use that connection.
                api.Backend.rpcclient.disconnect()
                if self.backoff:
                    self.__backoff(message_id)
                else:
                    raise

    def _ipa_client_configured(self):
        """Determine if the machine is an enrolled IPA client.

           Return boolean indicating whether this machine is enrolled
           in IPA. This is a rather weak detection method but better
           than nothing.
        """

        return os.path.exists('/etc/ipa/default.conf')


class IPAClient(IPANovaJoinBase):

    # TODO(jaosorior): Make the cache time and ttl configurable
    host_cache = cachetools.TTLCache(maxsize=512, ttl=30)
    service_cache = cachetools.TTLCache(maxsize=512, ttl=30)

    def add_host(self, hostname, ipaotp, metadata=None, image_metadata=None,
                 instance_id=None, message_id=0):
        """Add a host to IPA.


        If requested in the metadata, add a host to IPA. The assumption
        is that hostname is already fully-qualified.

        Because this is triggered by a metadata request, which can happen
        multiple times, first we try to update the OTP in the host entry
        and if that fails due to NotFound the host is added.

        Returns:
        Unicode Str: When a new host is added successfully, its OTP is returned
        This is later used to enroll the host via cloud-init
        False: Returned when host with same hostname and nova instance-id is
               already enrolled in IPA.
        DuplicateInstanceError: This is raised when an attempt is made to add
               a hostname that already exists and is enrolled in IPA.
        """

        LOG.debug("[%s] Adding %s to IPA.", message_id, hostname)

        if not self._ipa_client_configured():
            LOG.debug('[%s] IPA is not configured', message_id)
            return False

        # There's no use in doing any operations if ipalib hasn't been
        # imported.
        if not ipalib_imported:
            return True

        if metadata is None:
            metadata = {}
        if image_metadata is None:
            image_metadata = {}

        if hostname in self.host_cache:
            LOG.debug("[%s] Host  %s found in cache.", message_id, hostname)
            return self.host_cache[hostname]

        params = [hostname]

        hostclass = metadata.get('ipa_hostclass', '')
        location = metadata.get('ipa_host_location', '')
        osdistro = image_metadata.get('os_distro', '')
        osver = image_metadata.get('os_version', '')
        # 'description': 'IPA host for %s' % inst.display_description,

        novajoin_metadata = {"novajoin_metadata":
                             {"nova_instance_id": instance_id}}
        hostargs = {
            'description': six.text_type(json.dumps(novajoin_metadata)),
            'userpassword': six.text_type(ipaotp),
            'force': True  # we don't have an ip addr yet so
                           # use force to add anyway
        }
        if hostclass:
            hostargs['userclass'] = hostclass
        if osdistro or osver:
            hostargs['nsosversion'] = '%s %s' % (osdistro, osver)
            hostargs['nsosversion'] = hostargs['nsosversion'].strip()
        if location:
            hostargs['nshostlocation'] = location

        modargs = {
            'userpassword': six.text_type(ipaotp),
        }
        try:
            self._call_ipa(message_id, 'host_mod', *params, **modargs)
            self.host_cache[hostname] = six.text_type(ipaotp)
        except errors.NotFound:
            # No host with this hostname is presently enrolled in IPA
            try:
                self._call_ipa(message_id, 'host_add', *params, **hostargs)
                self.host_cache[hostname] = six.text_type(ipaotp)
            except errors.DuplicateEntry:
                # We have no idea what the OTP is for the existing host.
                return False
            except (errors.ValidationError, errors.DNSNotARecordError):
                # Assumes despite these exceptions the host was created
                # and the OTP was set.
                self.host_cache[hostname] = six.text_type(ipaotp)
        except errors.ValidationError:
            # A host with the same hostname is already enrolled in IPA.
            # Updating the OTP on an enrolled-host is not allowed
            # in IPA and really a no-op.

            # Note(hrybacki): Fetch host details from IPA and try to compare
            #                 the requested instance ID with what is stored
            #                 in IPA
            target_host = self._call_ipa(message_id, 'host_show', hostname)
            try:
                novajoin_metadata = json.loads(target_host['result']
                                               ['description'][0])
                stored_host_instance_id = \
                    novajoin_metadata['novajoin_metadata']['nova_instance_id']
                if stored_host_instance_id != instance_id:
                    LOG.error('[%s] %s already exists and is enrolled ' +
                              'with IPA. It was created for nova ' +
                              'instance %s. Requested host add originates ' +
                              'from nova instance %s. Please review and ' +
                              'manually remove host entries in IPA or choose' +
                              'another hostname before deploying the nova ' +
                              'instance again.',
                              message_id, hostname,
                              stored_host_instance_id, instance_id)
                    # NOTE(hrybacki): When we know the new host's instance-id
                    #                 does not match the enrolled host's, tell
                    #                 Nova to put the new compute node in an
                    #                 ERROR state
                    raise exception.DuplicateInstanceError(
                        hostname=hostname,
                        stored_instance_id=stored_host_instance_id,
                        instance_id=instance_id)
            except ValueError:
                # Note(hrybacki): Older host entries will have a unicode str
                #                 rather than a serialized json returned in
                #                 their Description field
                stored_host_instance_id = 'unknown'
                LOG.error('[%s] %s already exists and is enrolled with ' +
                          'IPA. This is an older host and novajoin is ' +
                          'unable to determine if the new host (%s) is ' +
                          'the same as the host in IPA. Please review ' +
                          'and manually remove host entries in IPA before ' +
                          'deploying the nova instance.',
                          message_id, hostname, instance_id)
                raise exception.DuplicateInstanceError(
                    hostname=hostname,
                    stored_instance_id=stored_host_instance_id,
                    instance_id=instance_id)
            else:
                # Note(hrybacki): The host is already enrolled, do nothing.
                LOG.info('OTP is unknown for host %s. This is because '
                         'validation failed during host_mod operation, '
                         'which means the host with the same name was '
                         'already enrolled.', hostname)
                return False

        return self.host_cache.get(hostname, False)

    def add_subhost(self, hostname, message_id=0):
        """Add a subhost to IPA.

        Servers can have multiple network interfaces, and therefore can
        have multiple aliases.  Moreover, they can part of a service using
        a virtual host (VIP).  These aliases are denoted 'subhosts',
        """
        LOG.debug('[%s] Adding subhost: %s', message_id, hostname)
        if hostname not in self.host_cache:
            params = [hostname]
            hostargs = {'force': True}
            self._add_batch_operation('host_add', *params, **hostargs)
            self.host_cache[hostname] = True
        else:
            LOG.debug("[%s] subhost %s found in cache.", message_id, hostname)

    def delete_subhost(self, hostname, batch=True, message_id=0):
        """Delete a subhost from IPA.

        Servers can have multiple network interfaces, and therefore can
        have multiple aliases.  Moreover, they can part of a service using
        a virtual host (VIP).  These aliases are denoted 'subhosts',
        """
        LOG.debug(" [%s] Deleting subhost: %s", message_id, hostname)
        host_params = [hostname]

        (hn, domain) = self.split_hostname(hostname)

        dns_params = [domain, hn]

        # If there is no DNS entry, this operation fails
        host_kw = {'updatedns': False, }

        dns_kw = {'del_all': True, }

        if batch:
            if hostname in self.host_cache:
                del self.host_cache[hostname]
            self._add_batch_operation('host_del', *host_params, **host_kw)
            self._add_batch_operation('dnsrecord_del', *dns_params,
                                      **dns_kw)
        else:
            if hostname in self.host_cache:
                del self.host_cache[hostname]
            self._call_ipa(message_id, 'host_del', *host_params, **host_kw)
            try:
                self._call_ipa(message_id, 'dnsrecord_del',
                               *dns_params, **dns_kw)
            except (errors.NotFound, errors.ACIError):
                # Ignore DNS deletion errors
                pass

    def delete_host(self, hostname, requested_instance_id, metadata=None,
                    message_id=0):
        """Delete a host from IPA and remove all related DNS entries."""
        LOG.debug("[%s] Deleting %s from IPA", message_id, hostname)

        if not self._ipa_client_configured():
            LOG.debug('[%s] IPA is not configured', message_id)
            return

        if metadata is None:
            metadata = {}

        target_host_instance_id = None
        try:
            # Note(hrybacki): Fetch host details from IPA and ensure we do not
            #                 delete a host entry if its instance-id does not
            #                 match the request
            target_host = self._call_ipa(message_id, 'host_show', hostname)
            novajoin_metadata = json.loads(target_host['result']
                                           ['description'][0])
            target_host_instance_id = \
                novajoin_metadata['novajoin_metadata']['nova_instance_id']
            if target_host_instance_id != requested_instance_id:
                LOG.info('Leaving %s in place. Deletion request instance-id ' +
                         '(%s) does not match instance-id mapped to host in ' +
                         'IPA (%s). This could be the result of an old, ' +
                         'cached delete request.',
                         hostname, requested_instance_id,
                         target_host_instance_id)
                raise exception.DeleteInstanceIdMismatch(
                    hostname=hostname,
                    requested_instance=requested_instance_id,
                    stored_instance=target_host_instance_id)
        except errors.NotFound:
            # NOTE(hrybacki): No host found. Continue and clean up the DNS
            #                 records.
            pass
        except ValueError:
            # NOTE(hrybacki): If we catch this, we are likely dealing with a
            #                 host that was created using an older version of
            #                 novajoin and does not contain the json object
            #                 with our metadata. Continue deletion of host,
            #                 subhosts, and dns records.
            pass

        params = [hostname]
        kw = {
            'updatedns': False,
        }
        try:
            if hostname in self.host_cache:
                del self.host_cache[hostname]
            self._call_ipa(message_id, 'host_del', *params, **kw)
        except (errors.NotFound, errors.ACIError):
            # Trying to delete a host that doesn't exist will raise an
            # ACIError to hide whether the entry exists or not
            pass

        (hn, domain) = self.split_hostname(hostname)

        dns_params = [domain, hn]

        dns_kw = {'del_all': True, }

        try:
            self._call_ipa(message_id, 'dnsrecord_del', *dns_params,
                           **dns_kw)
        except (errors.NotFound, errors.ACIError):
            # Ignore DNS deletion errors
            pass

    def add_service(self, principal, message_id=0):
        if principal not in self.service_cache:
            try:
                (service, hostname, realm) = self.split_principal(principal)
            except errors.MalformedServicePrincipal as e:
                LOG.error("[%s] Unable to split principal %s: %s",
                          message_id, principal, e)
                raise
            LOG.debug("[%s] Adding service: %s", message_id, principal)
            params = [principal]
            service_args = {'force': True}
            self._add_batch_operation('service_add', *params, **service_args)
            self.service_cache[principal] = [hostname]
        else:
            LOG.debug("[%s] Service %s found in cache", message_id, principal)

    def service_add_host(self, service_principal, host, message_id=0):
        """Add a host to a service.

        In IPA there is a relationship between a host and the services for
        that host. The host has the right to manage keytabs and SSL
        certificates for its own services. There are reasons that a host
        may want to manage services for another host or service:
        virtualization, load balancing, etc. In order to do this you mark
        the host or service as being "managed by" another host. For services
        in IPA this is done using the service-add-host API.
        """
        if host not in self.service_cache.get(service_principal, []):
            LOG.debug("[%s] Adding principal %s to host %s",
                      message_id, service_principal, host)
            params = [service_principal]
            service_args = {'host': (host,)}
            self._add_batch_operation('service_add_host', *params,
                                      **service_args)
            self.service_cache[service_principal] = self.service_cache.get(
                service_principal, []) + [host]
        else:
            LOG.debug("[%s] Host %s managing %s found in cache",
                      message_id, host, service_principal)

    def service_has_hosts(self, service_principal, message_id=0):
        """Return True if hosts other than parent manages this service"""

        LOG.debug("[%s] Checking if principal %s has hosts",
                  message_id, service_principal)
        params = [service_principal]
        service_args = {}
        try:
            result = self._call_ipa(message_id, 'service_show',
                                    *params, **service_args)
        except errors.NotFound:
            raise KeyError
        serviceresult = result['result']

        try:
            (service, hostname, realm) = self.split_principal(
                service_principal
            )
        except errors.MalformedServicePrincipal as e:
            LOG.error("[%s] Unable to split principal %s: %s",
                      message_id, service_principal, e)
            raise

        for candidate in serviceresult.get('managedby_host', []):
            if candidate != hostname:
                return True
        return False

    def host_get_services(self, service_host, message_id=0):
        """Return list of services this host manages"""
        LOG.debug("[%s] Checking host %s services", message_id, service_host)
        params = []
        service_args = {'man_by_host': six.text_type(service_host)}
        result = self._call_ipa(message_id, 'service_find',
                                *params, **service_args)
        return [service['krbprincipalname'][0] for service in result['result']]

    def host_has_services(self, service_host, message_id=0):
        """Return True if this host manages any services"""
        return len(self.host_get_services(service_host, message_id)) > 0

    def find_host(self, hostname, message_id=0):
        """Return True if this host exists"""
        LOG.debug("[%s] Checking if host %s exists", message_id, hostname)
        params = []
        service_args = {'fqdn': six.text_type(hostname)}
        result = self._call_ipa(message_id, 'host_find',
                                *params, **service_args)
        return result['count'] > 0

    def delete_service(self, principal, batch=True, message_id=0):
        LOG.debug("[%s] Deleting service: %s", message_id, principal)
        params = [principal]
        service_args = {}
        if batch:
            if principal in self.service_cache:
                del self.service_cache[principal]
            self._add_batch_operation('service_del', *params, **service_args)
        else:
            if principal in self.service_cache:
                del self.service_cache[principal]
            return self._call_ipa(message_id, 'service_del',
                                  *params, **service_args)

    def add_ip(self, hostname, floating_ip, message_id=0):
        """Add a floating IP to a given hostname."""
        LOG.debug("[%s] In add_ip", message_id)

        if not self._ipa_client_configured():
            LOG.debug('[%s] IPA is not configured', message_id)
            return

        params = [six.text_type(get_domain() + '.'),
                  six.text_type(hostname)]
        kw = {'a_part_ip_address': six.text_type(floating_ip)}

        try:
            self._call_ipa(message_id, 'dnsrecord_add', *params, **kw)
        except (errors.DuplicateEntry, errors.ValidationError):
            pass

    def find_record(self, floating_ip, message_id=0):
        """Find DNS A record for floating IP address"""
        LOG.debug("[%s] looking up host for floating ip %s",
                  message_id, floating_ip)
        params = [six.text_type(get_domain() + '.')]
        service_args = {'arecord': six.text_type(floating_ip)}
        result = self._call_ipa(message_id, 'dnsrecord_find',
                                *params, **service_args)
        if result['count'] == 0:
            return
        assert(result['count'] == 1)
        return result['result'][0]['idnsname'][0].to_unicode()

    def remove_ip(self, floating_ip, message_id=0):
        """Remove a floating IP from a given hostname."""
        LOG.debug("[%s] In remove_ip", message_id)

        if not self._ipa_client_configured():
            LOG.debug("[%s] IPA is not configured", message_id)
            return

        hostname = self.find_record(floating_ip, message_id)
        if not hostname:
            LOG.debug("[%s] floating IP record not found for %s",
                      message_id, floating_ip)
            return

        params = [six.text_type(get_domain() + '.'), hostname]
        service_args = {'arecord': six.text_type(floating_ip)}

        self._call_ipa(message_id, 'dnsrecord_del',
                       *params, **service_args)
