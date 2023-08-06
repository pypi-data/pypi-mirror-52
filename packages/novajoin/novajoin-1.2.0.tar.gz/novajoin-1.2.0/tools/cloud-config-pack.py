#!/usr/bin/env python

import json

with open('files/cloud-config-novajoin.yaml') as config_unpacked:
    config = config_unpacked.read()
    with open('files/cloud-config-novajoin.json', 'w') as cloud_config:
        json.dump({'cloud-init': config}, cloud_config)
        cloud_config.write('\n')
