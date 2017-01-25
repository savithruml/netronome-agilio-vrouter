# EXAMPLE TESTBED WITH 1 CONTROLLER & 2 COMPUTES

# Author: SAVITHRU LOKANATH
# Contact: SAVITHRU AT JUNIPER.NET
# Copyright (c) 2016 Juniper Networks, Inc. All rights reserved.

from fabric.api import env

host1 = 'root@192.168.1.1'
host2 = 'root@192.168.1.2'
host3 = 'root@192.168.1.3'

ext_routers = []

router_asn = 64512

host_build = 'root@192.168.1.1'

env.roledefs = {
    'all': [host1,host2,host3],
    'cfgm': [host1],
    'openstack': [host1],
    'control': [host1],
    'compute': [host1,host2],
    'collector': [host1],
    'webui': [host1],
    'database': [host1],
    'build': [host_build],
    'storage-master': [host1],
    'storage-compute': [host1],
}

env.openstack_admin_password = 'secret123'

env.hostnames = {
    host1: 'controller',
    host2: 'compute-1',
    host3: 'compute-2',
}

env.passwords = {
    host1: 'secret123',
    host2: 'secret123',
    host3: 'secret123',
    host_build: 'secret123',
}

minimum_diskGB = 50

control_data = {
    host1 : { 'ip': '172.31.255.1/24', 'gw' : '172.31.255.1', 'device': 'eth1' },
    host2 : { 'ip': '172.31.255.2/24', 'gw' : '172.31.255.1', 'device': 'nfp_p0' },
    host3 : { 'ip': '172.31.255.3/24', 'gw' : '172.31.255.1', 'device': 'nfp_p0' },
}

env.ns_agilio_vrouter = {
    host2: {'huge_page_alloc': '24G', 'huge_page_size': '1G', 'coremask': '2,4', 'pinning_mode': 'auto:split',
    host3: {'huge_page_alloc': '24G', 'huge_page_size': '1G', 'coremask': '2,4', 'pinning_mode': 'auto:split'}
}
