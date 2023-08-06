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
#
# To enable in nova, put this into [DEFAULT]
# notification_driver = messaging
# notification_topic = notifications
# notify_on_state_change = vm_state

import sys
import time

import glanceclient as glance_client
from neutronclient.v2_0 import client as neutron_client
from novaclient import client as nova_client
from oslo_log import log as logging
import oslo_messaging
from oslo_serialization import jsonutils

from novajoin import config
from novajoin import exception
from novajoin.ipa import IPAClient
from novajoin import join
from novajoin.keystone_client import get_session
from novajoin.keystone_client import register_keystoneauth_opts
from novajoin.nova import get_instance
from novajoin import util


CONF = config.CONF

LOG = logging.getLogger(__name__)


def ipaclient():
    return IPAClient()


def novaclient():
    session = get_session()
    return nova_client.Client('2.1', session=session)


def neutronclient():
    session = get_session()
    return neutron_client.Client(session=session)


def glanceclient():
    session = get_session()
    return glance_client.Client('2', session=session)


class Registry(dict):
    def __call__(self, name, version=None, service='nova'):
        def register_event(fun):
            if version:
                def check_event(sself, payload, message_id):
                    self.check_version(payload, version, service)
                    return fun(sself, payload[service + '_object.data'],
                               message_id)
                self[name] = check_event
                return check_event
            self[name] = fun
            return fun
        return register_event

    @staticmethod
    def check_version(payload, expected_version, service):
        """Check nova notification version

        If actual's major version is different from expected, a
        NotificationVersionMismatch error is raised.
        If the minor versions are different, a DEBUG level log
        message is output
        """
        notification_version = payload[service + '_object.version']
        notification_name = payload[service + '_object.name']

        maj_ver, min_ver = map(int, notification_version.split('.'))
        expected_maj, expected_min = map(int, expected_version.split('.'))
        if maj_ver != expected_maj:
            raise exception.NotificationVersionMismatch(
                provided_maj=maj_ver, provided_min=min_ver,
                expected_maj=expected_maj, expected_min=expected_min,
                type=notification_name)

        if min_ver != expected_min:
            LOG.debug(
                "Notification %(type)s minor version mismatch, "
                "provided: %(provided_maj)s.%(provided_min)s, "
                "expected: %(expected_maj)s.%(expected_min)s.",
                {"type": notification_name,
                 "provided_maj": maj_ver, "provided_min": min_ver,
                 "expected_maj": expected_maj, "expected_min": expected_min}
            )


class NotificationEndpoint(object):

    filter_rule = oslo_messaging.notify.filter.NotificationFilter(
        publisher_id='^compute.*|^network.*',
        event_type='^compute.instance.create.end|'
                   '^compute.instance.delete.end|'
                   '^compute.instance.update|'
                   '^network.floating_ip.(dis)?associate|'
                   '^floatingip.update.end')

    event_handlers = Registry()

    def info(self, ctxt, publisher_id, event_type, payload, metadata):
        LOG.debug('notification:')
        LOG.debug(jsonutils.dumps(payload, indent=4))

        LOG.debug("publisher: %s, event: %s, metadata: %s", publisher_id,
                  event_type, metadata)

        message_id = metadata['message_id']

        event_handler = self.event_handlers.get(
            event_type, lambda payload: LOG.error("Status update or unknown"))
        # run event handler for received notification type
        event_handler(self, payload, message_id)

    @event_handlers('compute.instance.create.end')
    def compute_instance_create(self, payload, message_id):
        hostname = self._generate_hostname(payload.get('hostname'))
        instance_id = payload['instance_id']
        LOG.info("[%s] Add new host %s (%s)",
                 message_id, instance_id, hostname)

    @event_handlers('compute.instance.update')
    def compute_instance_update(self, payload, message_id):
        ipa = ipaclient()
        join_controller = join.JoinController(ipa)
        hostname_short = payload['hostname']
        instance_id = payload['instance_id']
        payload_metadata = payload['metadata']
        image_metadata = payload['image_meta']

        hostname = self._generate_hostname(hostname_short)

        enroll = payload_metadata.get('ipa_enroll', '')
        image_enroll = image_metadata.get('ipa_enroll', '')
        if enroll.lower() != 'true' and image_enroll.lower() != 'true':
            LOG.info(
                '[%s] IPA enrollment not requested, skipping update of %s',
                message_id, hostname)
            return
        # Ensure this instance exists in nova
        instance = get_instance(instance_id)
        if instance is None:
            msg = '[%s] No such instance-id, %s' % (message_id, instance_id)
            LOG.error(msg)
            return

        LOG.info("[%s] compute instance update for %s", message_id, hostname)

        ipa.start_batch_operation(message_id)
        # key-per-service
        managed_services = [
            payload_metadata[key] for key in payload_metadata.keys()
            if key.startswith('managed_service_')]
        if managed_services:
            join_controller.add_managed_services(
                hostname, managed_services, message_id)

        compact_services = util.get_compact_services(payload_metadata)
        if compact_services:
            join_controller.add_compact_services(
                hostname_short, compact_services, message_id)

        ipa.flush_batch_operation(message_id)

    @event_handlers('compute.instance.delete.end')
    def compute_instance_delete(self, payload, message_id):
        hostname_short = payload['hostname']
        requested_instance_id = payload['instance_id']
        payload_metadata = payload['metadata']
        image_metadata = payload['image_meta']

        hostname = self._generate_hostname(hostname_short)

        enroll = payload_metadata.get('ipa_enroll', '')
        image_enroll = image_metadata.get('ipa_enroll', '')

        if enroll.lower() != 'true' and image_enroll.lower() != 'true':
            LOG.info(
                '[%s] IPA enrollment not requested, skipping delete of %s',
                message_id, hostname)
            return

        LOG.info("[%s] Delete host %s (%s)", message_id,
                 requested_instance_id, hostname)
        try:
            ipa = ipaclient()
            ipa.delete_host(hostname, requested_instance_id, {}, message_id)
            self.delete_subhosts(ipa, hostname_short, payload_metadata,
                                 message_id)
        except exception.IPAConnectionError:
            LOG.error("[%s] IPA Connection Error when deleting host %s (%s). "
                      "Manual cleanup may be required in the IPA server.",
                      message_id, requested_instance_id, hostname)
        except exception.DeleteInstanceIdMismatch:
            return

    @event_handlers('network.floating_ip.associate')
    def floaitng_ip_associate(self, payload, message_id):
        floating_ip = payload['floating_ip']
        LOG.info("[%s] Associate floating IP %s" % (message_id, floating_ip))
        ipa = ipaclient()
        nova = novaclient()
        server = nova.servers.get(payload['instance_id'])
        if server:
            ipa.add_ip(server.name, floating_ip, message_id)
        else:
            LOG.error("[%s] Could not resolve %s into a hostname",
                      message_id, payload['instance_id'])

    @event_handlers('network.floating_ip.disassociate')
    def floating_ip_disassociate(self, payload, message_id):
        floating_ip = payload['floating_ip']
        LOG.info("[%s] Disassociate floating IP %s", message_id, floating_ip)
        ipa = ipaclient()
        ipa.remove_ip(floating_ip, message_id)

    @event_handlers('floatingip.update.end')
    def floating_ip_update(self, payload, message_id):
        """Neutron event"""
        floatingip = payload['floatingip']
        floating_ip = floatingip['floating_ip_address']
        port_id = floatingip['port_id']
        ipa = ipaclient()
        if port_id:
            LOG.info("[%s] Neutron floating IP associate: %s",
                     message_id, floating_ip)
            nova = novaclient()
            neutron = neutronclient()
            search_opts = {'id': port_id}
            ports = neutron.list_ports(**search_opts).get('ports')
            if len(ports) == 1:
                device_id = ports[0].get('device_id')
                if device_id:
                    server = nova.servers.get(device_id)
                    if server:
                        ipa.add_ip(server.name, floating_ip, message_id)
            else:
                LOG.error("[%s] Expected 1 port, got %d",
                          message_id, len(ports))
        else:
            LOG.info("[%s] Neutron floating IP disassociate: %s",
                     message_id, floating_ip)
            ipa.remove_ip(floating_ip, message_id)

    def delete_subhosts(self, ipa, hostname_short, metadata, message_id):
        """Delete subhosts and remove VIPs if possible.

        Servers can have multiple network interfaces, and therefore can
        have multiple aliases.  Moreover, they can part of a service using
        a virtual host (VIP).  These aliases are denoted 'subhosts',

        We read the metadata to determine which subhosts to remove.

        The subhosts corresponding to network aliases are specified in the
        metadata parameter compact_services.  These are specified in a compact
        JSON representation to avoid the 255 character nova metadata limit.
        These should all be removed when the server is removed.

        The VIPs should only be removed if the host is the last host managing
        the service.
        """
        if metadata is None:
            return

        compact_services = util.get_compact_services(metadata)
        if compact_services:
            self.delete_compact_services(ipa, hostname_short,
                                         compact_services,
                                         message_id)
        managed_services = [metadata[key] for key in metadata.keys()
                            if key.startswith('managed_service_')]
        if managed_services:
            self.delete_managed_services(ipa, managed_services, message_id)

    def delete_compact_services(self, ipa, host_short, service_repr,
                                message_id):
        """Reconstructs and removes subhosts for compact services.

           Data looks like this:
            {"HTTP":
                ["internalapi", "ctlplane", "storagemgmt", "storage"],
             "rabbitmq":
                ["internalapi", "ctlplane"]
            }

            In this function, we will remove the subhosts.  We expect the
            services to be automatically deleted through IPA referential
            integrity.
        """
        LOG.debug("[%s] In delete compact services", message_id)
        hosts_found = list()

        ipa.start_batch_operation(message_id)
        for service_name, net_list in service_repr.items():
            for network in net_list:
                host = "%s.%s" % (host_short, network)
                principal_host = util.get_fqdn(host)

                # remove host
                if principal_host not in hosts_found:
                    ipa.delete_subhost(principal_host)
                    hosts_found.append(principal_host)
        ipa.flush_batch_operation(message_id)

    def delete_managed_services(self, ipa, services, message_id):
        """Delete any managed services if possible.

           Checks to see if the managed service subhost has no managed hosts
           associations and if so, deletes the host.
        """
        LOG.debug("[%s] In delete_managed_services", message_id)
        hosts_deleted = list()
        services_deleted = list()

        for principal in services:
            if principal not in services_deleted:
                try:
                    if ipa.service_has_hosts(principal):
                        continue
                except KeyError:
                    continue
                ipa.delete_service(principal, batch=False)
                services_deleted.append(principal)

            principal_host = principal.split('/', 1)[1]
            if principal_host not in hosts_deleted:
                if not ipa.host_has_services(principal_host):
                    ipa.delete_subhost(principal_host, batch=False)
                    hosts_deleted.append(principal_host)

    def _generate_hostname(self, hostname):
        # FIXME: Don't re-calculate the hostname, fetch it from somewhere
        project = 'foo'
        domain = util.get_domain()
        if CONF.project_subdomain:
            host = '%s.%s.%s' % (hostname, project, domain)
        else:
            host = '%s.%s' % (hostname, domain)
        return host


class VersionedNotificationEndpoint(NotificationEndpoint):

    filter_rule = oslo_messaging.notify.filter.NotificationFilter(
        publisher_id='^nova-compute.*|^network.*',
        event_type='^instance.create.end|'
                   '^instance.delete.end|'
                   '^instance.update|'
                   '^floatingip.update.end')

    event_handlers = Registry(NotificationEndpoint.event_handlers)

    @event_handlers('instance.create.end', '1.10')
    def instance_create(self, payload, message_id):
        newpayload = {
            'hostname': payload['host_name'],
            'instance_id': payload['uuid'],
        }
        self.compute_instance_create(newpayload, message_id)

    @event_handlers('instance.update', '1.8')
    def instance_update(self, payload, message_id):
        glance = glanceclient()
        newpayload = {
            'hostname': payload['host_name'],
            'instance_id': payload['uuid'],
            'metadata': payload['metadata'],
            'image_meta': glance.images.get(payload['image_uuid'])
        }
        self.compute_instance_update(newpayload, message_id)

    @event_handlers('instance.delete.end', '1.7')
    def instance_delete(self, payload, message_id):
        glance = glanceclient()
        newpayload = {
            'hostname': payload['host_name'],
            'instance_id': payload['uuid'],
            'metadata': payload['metadata'],
            'image_meta': glance.images.get(payload['image_uuid'])
        }
        self.compute_instance_delete(newpayload, message_id)


def main():
    register_keystoneauth_opts(CONF)
    CONF(sys.argv[1:], version='1.2.0',
         default_config_files=config.find_config_files())
    logging.setup(CONF, 'join')

    transport = oslo_messaging.get_notification_transport(CONF)
    targets = [oslo_messaging.Target(topic=CONF.notifications_topic)]
    if CONF.notification_format == 'unversioned':
        endpoints = [NotificationEndpoint()]
    elif CONF.notification_format == 'versioned':
        endpoints = [VersionedNotificationEndpoint()]

    server = oslo_messaging.get_notification_listener(transport,
                                                      targets,
                                                      endpoints,
                                                      executor='threading')
    LOG.info("Starting")
    server.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        LOG.info("Stopping, be patient")
        server.stop()
        server.wait()
