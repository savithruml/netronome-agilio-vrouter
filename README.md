# Contrail-Netronome Architecture
  ![architecture](https://github.com/savithruml/netronome-agilio-vrouter/blob/3.1.2/images/contrail_agilio_architecture.png)
  
# Lab Setup
  ![lab setup](https://github.com/savithruml/netronome-agilio-vrouter/blob/3.1.2/images/lab_setup.png)

# Pre-Requisites

* Ubuntu 14.04.4 (3.13.0-100 Errata 47 patched kernel)
* Contrail-Cloud 3.1.2.0-65 (OpenStack Kilo/Mitaka)
* Agilio vRouter 3.1.0.0-124

# Netronome SmartNic Install Guide

NOTE: This guide assumes that you have already inserted the Netronome NIC on the server. For a list of supported servers, refer this [document](https://github.com/savithruml/netronome-agilio-vrouter/blob/3.1.2/list-of-supported-servers.pdf)

## On all nodes
* Install Ubuntu 14.04.4 on all the nodes in the setup

* Download & install Contrail packages on the nodes

         (all-nodes)# dpkg -i contrail-install-packages_3.1.2.0-65~mitaka_all.deb
         (all-nodes)# /opt/contrail/contrail_packages/setup.sh
         (all-nodes)# apt-get update

* Download Netronome (Agilio vRouter) package & copy to all nodes

         (all-nodes)# tar -xvf ns-agilio-vrouter-release_3.1.0.0-124.tgz 
         (all-nodes)# cd ns-agilio-vrouter-release_3.1.0.0-124/
         (all-nodes)# cp ns-agilio-vrouter-depends-packages_3.1.0.0-124_amd64.deb /opt/contrail/contrail_install_repo/
         (all-nodes)# cd /opt/contrail/contrail_install_repo/
         (all-nodes)# dpkg-scanpackages . /dev/null | gzip -9c > Packages.gz
         (all-nodes)# apt-get update
         
## On Controller node

* Populate testbed with relevant information

         (controller-node)# vim /opt/contrail/utils/fabfile/testbeds/testbed.py
         
         
                  bond= {
                      compute-1 : { 'name': 'bond0', 'member': ['nfp_p0','nfp_p1','nfp_p2','nfp_p3'], 'mode': '802.3ad',    
                                'xmit_hash_policy': 'layer3+4' },
                      compute-2 : { 'name': 'bond0', 'member': ['nfp_p0','nfp_p1','nfp_p2','nfp_p3'], 'mode': '802.3ad',    
                                'xmit_hash_policy': 'layer3+4' },
                  }
                  
                  control_data = {
                      controller : { 'ip': '172.31.255.1/24', 'gw' : '172.31.255.1', 'device': 'eth1' },
                      compute-1 : { 'ip': '172.31.255.2/24', 'gw' : '172.31.255.1', 'device': 'bond0' },
                      compute-2 : { 'ip': '172.31.255.3/24', 'gw' : '172.31.255.1', 'device': 'bond0' },
                  }
         
                  env.ns_agilio_vrouter = {
                      compute-1: {'huge_page_alloc': '24G', 'huge_page_size': '1G', 'coremask': '2,4', 'pinning_mode': 
                                  'auto:split'},
                      compute-2: {'huge_page_alloc': '24G', 'huge_page_size': '1G', 'coremask': '2,4', 'pinning_mode': 
                                  'auto:split'}
                  }

  [Click for example files](https://github.com/savithruml/netronome-agilio-vrouter/blob/3.1.2/testbed)

* Bring up the Netronome SmartNIC

         (controller-node)# cd /opt/contrail/utils/
         (controller-node)# fab install_ns_agilio_nic
         
* Change the media configuration of the SmartNIC if you are using breakout cables (4 x 10GbE ---> 1 X 40GbE). This should create *FOUR* NFP interfaces: nfp_p0, nfp_p1, nfp_p2, nfp_p3

         (controller-node)# /opt/netronome/bin/nfp-media --set-media=phy0=4x10G
         (controller-node)# service ns-core-nic.autorun clean
         (controller-node)# reboot
         
* Install Contrail

         (controller-node)# cd /opt/contrail/utils
         (controller-node)# fab install_contrail
         (controller-node)# fab setup_interface (Verify if all nodes can talk with each other on Control/Data interface)
         (controller-node)# fab setup_all

## On Netronome compute node

* Verify if provisioning was successfully

         (compute-nodes)# contrail-status
         (compute-nodes)# /opt/netronome/libexec/nfp-vrouter-status -r

  ![Agilio-vRouter](https://github.com/savithruml/netronome-agilio-vrouter/blob/3.1.2/images/agilio_vrouter.png)

* Create VirtIO flavors

  NOTE: Do this only once

         (compute-node)# cd /ns-agilio-vrouter-release_3.1.0.0-124/ns-agilio-vrouter_3.1.0.0-124/opt/netronome/openstack
         (compute-node)# ./make_virtio_flavors.sh <controller-ip-address>
         
