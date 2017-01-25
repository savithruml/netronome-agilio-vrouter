# Contrail-Netronome Architecture
  ![architecture](https://github.com/savithruml/netronome-agilio-vrouter/blob/master/images/contrail_agilio_architecture.png)
  
# Lab Setup
  ![lab setup](https://github.com/savithruml/netronome-agilio-vrouter/blob/master/images/lab_setup.png)

# Netronome SmartNic Install Guide

NOTE: This guide assumes that you have already inserted the Netronome NIC on the server

## On all nodes
* Install Ubuntu 14.04.4 on all the nodes in the setup

* Download Netronome (Agilio vRouter) package & copy to all the nodes. Untar the copied file

         (all-nodes)# tar -xvf Agilio_vRouter_Juniper_Drop_7.tar
         (all-nodes)# cd Agilio_vRouter_Juniper_Drop_7/
         (all-nodes)# tar -xvf ns-agilio-vrouter-fab_3.1.0.0-11.tgz 
         (all-nodes)# tar -xvf agilio-vrouter_3.1.0.0_2016.11.21_build-11_3.13.0-100.tgz

* Install Contrail packages

         (all-nodes)# cd ns-agilio-vrouter-fab/
         (all-nodes)# dpkg -i contrail-install-packages_3.1.0.0-25~kilo_all.deb
         (all-nodes)# /opt/contrail/contrail_packages/setup.sh
         (all-nodes)# apt-get update

## On Netronome compute nodes

* Update Linux Kernel to the supported version

         (compute-nodes)# apt-get install linux-image-3.13.0-100-generic
         (compute-nodes)# apt-get install linux-headers-3.13.0-100-generic
         (compute-nodes)# apt-get install linux-image-extra-3.13.0-100-generic
         (compute-nodes)# apt-get install linux-image-generic
         (compute-nodes)# apt-get install linux-generic

* Update Grub & reboot

         (compute-nodes)# vim /etc/default/grub

                 Based on NUMA, modify to look as below,

                   GRUB_DEFAULT='1>Ubuntu, with Linux 3.13.0-100-generic'

                   GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"
                   with
                   GRUB_CMDLINE_LINUX_DEFAULT="intel_iommu=on iommu=pt intremap=on intel_idle.max_cstate=0             
                                               processor.max_cstate=0 idle=mwait intel_pstate=disable default_hugepagesz=1G  
                                               hugepagesz=1G hugepages=224 isolcpus=1-7,17-23,9-15, 25-31"

         (compute-nodes)# update-grub
         (compute-nodes)# reboot

## On all nodes

* Install Agilio vRouter packages

         (all-nodes)# cd Agilio_vRouter_Juniper_Drop_7/ns-agilio-vrouter-fab/
         (all-nodes)# cp ns-agilio-vrouter-depends-packages_3.1.0.0-11_amd64.deb /opt/contrail/contrail_install_repo/

         (all-nodes)# dpkg -i ns-agilio-vrouter-depends-packages_3.1.0.0-11_amd64.deb 
         (all-nodes)# /opt/contrail/contrail_packages_ns_agilio_vrouter/setup.sh
         (all-nodes)# cd /opt/contrail/contrail_install_repo
         (all-nodes)# dpkg-scanpackages . /dev/null | gzip -9c > Packages.gz
         (all-nodes)# apt-get update

* Copy patched Contrail fabric files

         (all-nodes)# cd Agilio_vRouter_Juniper_Drop_7/ns-agilio-vrouter-fab/
         (all-nodes)# cp fabfile/tasks/*.py /opt/contrail/utils/fabfile/tasks/
         (all-nodes)# cp fabfile/utils/*.py /opt/contrail/utils/fabfile/utils/

## On Netronome compute nodes

* Install coreNIC firmware & reboot 

  NOTE: Do this only once

         (compute-nodes)# apt-get install dkms libftdi1 libjansson4
         (compute-nodes)# cd Agilio_vRouter_Juniper_Drop_7/ns-agilio-vrouter-fab/
         (compute-nodes)# dpkg -i nfp-bsp-6000-b0*
         
         (compute-nodes)# ldconfig
         (compute-nodes)# modprobe nfp

         (compute-nodes)# /opt/netronome/bin/nfp-flash --i-accept-the-risk-of-overwriting-miniloader -w /opt/netronome/flash/flash-nic.bin
         (compute-nodes)# /opt/netronome/bin/nfp-one
         
                          press <ENTER> when prompted
         
         (compute-nodes)# reboot

         (compute-nodes)# cd Agilio_vRouter_Juniper_Drop_7/ns-agilio-vrouter-fab/
         (compute-nodes)# dpkg -i ns-agilio-core-nic_0-8_all.deb
         
         
  NOTE: This step is required if using breakout cables

         (compute-nodes)# /opt/netronome/bin/nfp-media --set-media=phy0=4x10G
         (compute-nodes)# service ns-core-nic.autorun clean

* Check if NFP interfaces were created

         (compute-nodes)# reboot
         (compute-nodes)# ifconfig | grep -i "nfp"

      ![ifconfig](https://github.com/savithruml/netronome-agilio-vrouter/blob/master/images/ifconfig.png)
         
## On Controller node

* Populate testbed with relevant information

         (controller-node)# vim /opt/contrail/utils/fabfile/testbeds/testbed.py
         
         
                  bond= {
                      compute-1 : { 'name': 'bond0', 'member': ['nfp_p0','nfp_p1'], 'mode': '802.3ad',    
                                'xmit_hash_policy': 'layer3+4' },
                      compute-2 : { 'name': 'bond0', 'member': ['nfp_p0','nfp_p1'], 'mode': '802.3ad',    
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

  [Click for example files](https://github.com/savithruml/netronome-agilio-vrouter/tree/master/testbed)

* Install Contrail

         (controller-node)# cd /opt/contrail/utils/
         (controller-node)# fab install_contrail
         (controller-node)# fab setup_interface (Verify if all nodes can talk with each other on Control/Data interface)

  ![Ping control/data interface](https://github.com/savithruml/netronome-agilio-vrouter/blob/master/images/control_data_ping.png)

         (controller-node)# fab setup_all
         (controller-node)# contrail-status

## On Netronome compute node

* Verify if provisioning was successfully

         (compute-nodes)# contrail-status
         (compute-nodes)# /opt/netronome/libexec/nfp-vrouter-status -r

  ![Agilio-vRouter](https://github.com/savithruml/netronome-agilio-vrouter/blob/master/images/agilio_vrouter.png)

* Create VirtIO flavors

  NOTE: Do this only once

         (compute-node)# cd Agilio_vRouter_Juniper_Drop_7/agilio-vrouter_3.1.0.0_2016.11.21_build-11_3.13.0-100/openstack/
         (compute-node)# ./make_virtio_flavors.sh <controller-ip-address>
         
