
### Ading a card in Qemu

    qemu -net nic,model=e1000 ...

### Others emulated architectures

    $ qemu-system-<arch> -net nic,model=?
      Supported NIC models: ne2k_pci,i82551,i82557b,i82559er,rtl8139,e1000,pcnet,virtio,sungem

## Ethernet Cards
### 3Com 501
- created in 1988 by 3Com.
- among the first card supported by Linux

### Intel E1000
- it is available on a variety of emulators such as VirtualBox, Qemu
- 1Gb/b
- PCI

### NE2000
- Produced by Novell in 1988s.
- it is a 16-bit ISA card.
- Emulated by Qemu

### RTL8139C : Realtek Fast Ethernet 
- 10/100 Mbits/s. PCI 2.2. 
- Wake-on-LAN from PCI bus(magic packet). 
- Emulated by Qemu


## How to write a driver
1. Detect the device
2. Enable the device
3. Understand the network device
4. Bus-independent device access
5. PCI configuration space
6. Initialise net_device
7. RealTek8139's transmission mechanism
8. RealTek8139's receiving mechanism
9. Making the device ready to transmit packets
10. Making the device ready to receive packets 




## References
- cours de Patrick Cegielski.  http://lacl.univ-paris12.fr/cegielski/reseau.html
- https://en.wikipedia.org/wiki/QEMU#Emulated_hardware_platforms
- https://wiki.osdev.org/Category:Network_Hardware
- https://wiki.osdev.org/Intel_Ethernet_i217
- http://www6.uniovi.es/LDP/LDP/LGNET/156/jangir.html
