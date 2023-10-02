### Clone a VM
After colning a VM:
1. Change the hostname:
  * /etc/hostname
  * /etc/hosts
2. Update the IP


### Netwoking:
1. NAT : Network Address Translation. 
   * Give internet access to Guest. Host cannot access to Guest. 
   * To create a NAT Adapter: File->Preferences->Network.
2. Host-only networking
   * VMs can talk to each other and the Host, as if they were connected through a physical switch.
   * VMs connot connect to internet or outside Host.
   * Create a network interface. File->Host Network Manager. Choose Host-Only Adapter in Guest network setting. 
   * IPs are given by DHCP like adapter.
   * On Geust
   ~~~
   $ ifconfig -a   ; find the mounted nic device. 
   $ nano /etc/network/interfaces
       auto enp0s3
       iface enp0s3 inet static
          address 10.98.56.101
          netmask 255.255.255.0
          broadcast 10.98.56.256
          gateway 10.98.56.1
   $ sudo /etc/init.d/networking restart
   ~~~
3. Bridged networking: 
   * Like Host-only.
   * moreover, VMs can communicate with outside the Host.
   
#### Shared folder
You must install VBox additions to use shared folders

shared folder permission denied
```
 sudo adduser your-user vboxsf
 sudo reboot now
```













