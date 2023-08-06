#!/usr/bin/env python

import json

with open('files/cloud-config-novajoin.json') as cloud_config:
    config = json.load(cloud_config)['cloud-init']
    with open('files/cloud-config-novajoin.yaml', 'w') as config_unpacked:
        config_unpacked.write(config)
