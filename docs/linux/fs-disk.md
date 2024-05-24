---
layout: default
title: File Systems - Disks
parent: Linux
nav_order: 3
---

### Create a New Partition
- Liste all partitions present on your system
~~~sh
# fdisk -l
~~~

- Create a Partition
~~~sh
# fdisk [disk path]
~~~

- Format the patition
~~~sh
# mkfs.ext4 [partition path]
~~~

### Mount a Partition
- Mount the partition
~~~sh
# mount -t ext4 /dev/sda2 /opt/appdynamics
~~~

- make it permanent: add to **/etc/fstab**
~~~
/dev/sda2       /opt/appdynamics ext4    defaults        0       0
~~~

- Check if it was mounted
~~~sh
# df -h
~~~


### Disk & FS
List all block devices:
 
    # lsblk

List Partitions Under Linux (case android)

    # fdisk -l /dev/block/mmcblk0 
    # fdisk -l -u=cylinders /sdcard1/qemu/qemu1.img

create a virtual disk of 1MB  

    dd if=/dev/zero of=disk.img bs=512 count=2000 	

Formate using ext2 FS
 
    # mkfs.ext2 -b 1024 disk.img
 
Dump disk infos 
 
    # dumpe2fs disk.img
    # sudo dumpe2fs /dev/sda7  ; for ext2/ext3/ext4

Mount a virtual disk(Android) : use terminalEmulator/root

    # mount -o rw,remount /
    # mkdir /mnt/tmp
    # busybox losetup /dev/block/loop0 /extSdCard/qemu/qemu1.img
    # busybox  mount -o loop -t auto /dev/block/loop0  /mnt/tmp
      then you can access the virtual img via /mnt/tmp dir.

Formating an USB or a disk partition

    # fdisk -l              ; identify the partition to formate
    # umount /dev/sdb1
    # mkfs.ntfs /dev/sdb1   ; we always formate a partition not the hole disk.
 
Online Resizing an FS

    # lvresize -L +4G /dev/VolPrddb/db1
    # lvresize -L +4G /dev/VolPrddb/db1
    # resize2fs -p /dev/VolPrddb/db1 +8G
    # resize2fs  /dev/VolPrddb/db1


### RAID
RAID 5 : https://www.dataretrieval.com/raid-data-recovery/raid-5-internals-data-storage-performance-and-recovery.html

### Create a ISO 9660 image
From a devide or cdrom 

    dd if=/dev/sda1 of=~/disk1_image.iso

From a directory  

    mkisofs -o /tmp/cd.iso /tmp/directory/ 

mount an iso file

    sudo mount /path/to/cd.iso /mnt/cdrom -o loop


### Ext4 FileSystem internals
Create and formate a disk image

    dd if=/dev/zero of=disk.img bs=512 count=2000 # 1MB image
    pkg install e2fsprogs
    mkfs -b 4096 -t ext4 disk.img # 4kB blocks

Dump an Inode

    stat employee.json

### Clean Disk Space
List of 10 biggest Directories

	du -h / | sort -hr | head -n 10

Sort files by size: `ls -lSr`

Clear Apt Cache

	apt clean


