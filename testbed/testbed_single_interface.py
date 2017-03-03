# EXAMPLE TESTBED WITH 1 CONTROLLER & 2 COMPUTES

# Author: SAVITHRU LOKANATH
# Contact: SAVITHRU AT JUNIPER.NET
# Copyright (c) 2017 Juniper Networks, Inc. All rights reserved.

from fabric.api import env

controller = 'root@192.168.1.1'
compute1 = 'root@192.168.1.2'
compute2 = 'root@192.168.1.3'

ext_routers = []

router_asn = 64512

host_build = 'root@192.168.1.1'

env.roledefs = {
    'all': [controller,compute1,compute2],
    'cfgm': [controller],
    'openstack': [controller],
    'control': [controller],
    'compute': [compute1,compute2],
    'collector': [controller],
    'webui': [controller],
    'database': [controller],
    'build': [host_build],
    'storage-master': [controller],
    'storage-compute': [controller],
}

env.openstack_admin_password = 'secret123'

env.hostnames = {
    controller: 'controller',
    compute1: 'compute1',
    compute2: 'compute2',
}

env.passwords = {
    controller: 'secret123',
    compute1: 'secret123',
    compute2: 'secret123',
    host_build: 'secret123',
}

minimum_diskGB = 50

control_data = {
    controller : { 'ip': '172.31.255.1/24', 'gw' : '172.31.255.1', 'device': 'eth1' },
    compute1 : { 'ip': '172.31.255.2/24', 'gw' : '172.31.255.1', 'device': 'nfp_p0' },
    compute2 : { 'ip': '172.31.255.3/24', 'gw' : '172.31.255.1', 'device': 'nfp_p0' },
}

env.ns_agilio_vrouter = {
    compute1: {'huge_page_alloc': '24G', 'huge_page_size': '1G', 'coremask': '2,4', 'pinning_mode': 'auto:split',
    compute2: {'huge_page_alloc': '24G', 'huge_page_size': '1G', 'coremask': '2,4', 'pinning_mode': 'auto:split'}
}
