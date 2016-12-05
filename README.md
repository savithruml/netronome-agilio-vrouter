# Netronome SmartNic Install Guide

NOTE: This guide assumes that you have already inserted the Netronome NIC on the server

## On all nodes
* Install Ubuntu 14.04.4 on all the nodes in the setup

* Download Netronome (Agilio vRouter) package & copy to all the nodes. Untar the copied file

         (all-nodes)# tar -xvf Agilio_vRouter_Juniper_Drop_6.tar
         (all-nodes)# cd Agilio_vRouter_Juniper_Drop_6/
         (all-nodes)# tar -xvf ns-agilio-vrouter-fab_3.0.2.0-187.tgz
         (all-nodes)# tar -xvf agilio-vrouter_3.0.2.0_2016.11.15_build-187_3.13.0-68.tgz

* Install Contrail packages

         (all-nodes)# cd ns-agilio-vrouter-fab/
         (all-nodes)# dpkg -i contrail-install-packages_3.0.2.0-51~kilo_all.deb
         (all-nodes)# /opt/contrail/contrail_packages/setup.sh
         (all-nodes)# apt-get update

## On Netronome compute nodes

* Update Linux Kernel to the supported version

         (compute-nodes)# cd ../agilio-vrouter_3.0.2.0_2016.11.15_build-187_3.13.0-68/deps/
         (compute-nodes)# tar -xvf linux-3.13.0-68-generic-nfp.tgz
         (compute-nodes)# cd linux-3.13.0-68-generic-nfp/
         (compute-nodes)# ./setup.sh

* Update Grub & reboot

         (compute-nodes)# vim /etc/default/grub

                 Replace

                   GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"
                   with
                   GRUB_CMDLINE_LINUX_DEFAULT="intel_iommu=on iommu=pt intremap=on"

         (compute-nodes)# update-grub
         (compute-nodes)# reboot

## On all nodes

* Install Agilio vRouter packages

         (all-nodes)# cd Agilio_vRouter_Juniper_Drop_6/ns-agilio-vrouter-fab/
         (all-nodes)# cp ns-agilio-vrouter-depends-packages_3.0.2.0-187_amd64.deb /opt/contrail/contrail_install_repo/

         (all-nodes)# dpkg -i ns-agilio-vrouter-depends-packages_3.0.2.0-187_amd64.deb
         (all-nodes)# /opt/contrail/contrail_packages_ns_agilio_vrouter/setup.sh
         (all-nodes)# cd /opt/contrail/contrail_install_repo
         (all-nodes)# dpkg-scanpackages . /dev/null | gzip -9c > Packages.gz
         (all-nodes)# apt-get update

* Copy patched Contrail fabric files

         (all-nodes)# cd Agilio_vRouter_Juniper_Drop_6/ns-agilio-vrouter-fab/
         (all-nodes)# cp fabfile/tasks/*.py /opt/contrail/utils/fabfile/tasks/
         (all-nodes)# cp fabfile/utils/*.py /opt/contrail/utils/fabfile/utils/

## On Netronome compute nodes

* Install coreNIC firmware & reboot 

  NOTE: Do this only once

         (compute-nodes)# apt-get install dkms libftdi1 libjansson4
         (compute-nodes)# cd Agilio_vRouter_Juniper_Drop_6/ns-agilio-vrouter-fab/
         (compute-nodes)# dpkg -i nfp-bsp-6000-b0*
         
         (compute-nodes)# ldconfig
         (compute-nodes)# mod probe nap

         (compute-nodes)# /opt/netronome/bin/nfp-flash --i-accept-the-risk-of-overwriting-miniloader -w /opt/netronome/flash/flash-nic.bin
         (compute-nodes)# /opt/netronome/bin/nfp-one
         (compute-nodes)# reboot

         (compute-nodes)# cd Agilio_vRouter_Juniper_Drop_6/ns-agilio-vrouter-fab/
         (compute-nodes)# dpkg -i ns-agilio-core-nic_0-8_all.deb

* Check if NFP interfaces were created

         (compute-nodes)# ifconfig | grep -i "nfp"

      ![ifconfig](https://github.com/savithruml/netronome-agilio-vrouter/blob/master/images/ifconfig.png)
         
## On Controller node

* Populate testbed with relevant information

         (controller-node)# vim /opt/contrail/utils/fabfile/testbeds/testbed.py
         
                  env.ns_agilio_vrouter = {
                      compute-1: {'huge_page_alloc': '24G', 'huge_page_size': '1G', 'coremask': '2,4', 'pinning_mode': 'auto:combine'},
                      compute-2: {'huge_page_alloc': '24G', 'huge_page_size': '1G', 'coremask': '2,4', 'pinning_mode': 'auto:combine'}
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

         
         
