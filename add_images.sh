# Author: SAVITHRU LOKANATH
# Contact: SAVITHRU AT JUNIPER.NET
# Copyright (c) 2017 Juniper Networks, Inc. All rights reserved.

# DESCRIPTION: Script to add images to OpenStack

#!/bin/bash

cd 
source /etc/contrail/openstackrc
mkdir images && cd images 
wget http://10.84.5.120/cs-shared//images/ubuntu.img.gz
wget http://10.84.5.120/cs-shared//images/analyzer/analyzer-vm-console.qcow2.gz
wget http://10.84.5.120/cs-shared//images/vsrx/junos-vsrx-12.1-in-network.img.gz
wget http://10.84.5.120/cs-shared//images/vsrx/junos-vsrx-12.1-transparent.img.gz
gunzip *gz
glance image-create --name ubuntu --visibility=public --container-format ovf --disk-format qcow2 --file ubuntu.img
glance image-create --name analyzer --visibility=public --container-format ovf --disk-format qcow2 --file analyzer-vm-console.qcow2
glance image-create --name vsrx-nat-service --visibility=public --container-format ovf --disk-format qcow2 --file junos-vsrx-12.1-in-network.img
glance image-create --name vsrx-transparent-service --visibility=public --container-format ovf --disk-format qcow2 --file junos-vsrx-12.1-transparent.img