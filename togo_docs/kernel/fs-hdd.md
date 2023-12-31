
## Hard Drive, IDE/ATA
![](/documentation/images/HDD-CHS.jpg)

Track = Head 

Cylinder 15 = Track 15 on platter 0 + track 15 on platter 1 + etc. 

- 2 Block Addressing methods
  * CHS - Cylinder/Head/Sector.
  * LBA - Logical Block Addressing.
    MBR is a sector with LBA=0. 
- LBA-to-CHS conversion :
~~~
  LBA = (C x TH x TS) + (H x TS) + (S - 1)
  Where:
  C = Cylinder
  TH = the Total Heads 
  TS = the Total Sectors/Track
  H = Head
  S = Sector
~~~  
  C, H, LBA start at 0. S start at 1. 

- MBR - Master Boot Record(512B or +):  may contain one or more of:
  * A partition table describing the partitions of a storage device. 
    In this context the boot sector may also be called a partition sector.
  * Bootstrap code: Instructions to identify the configured bootable partition, 
    then load and execute its volume boot record (VBR) as a chain loader.
  
- Disk partitions
  * fdisk : command to create partionning
  * there are exactly 4 primary partition table entries in the MBR partition table.
  * la table de partition est ecrit sur disk at byte number 446 exactely.
  * Structure of a classical generic MBR
  ~~~
    Address    Description        Size(bytes)
    (bytes)
    +0       Bootstrap code area  446
    +446     Partition entry 1     16
    +462     Partition entry 2     16
    +478     Partition entry 3     16
    +494     Partition entry 4     16
    +510     0x55 Boot signature    2
    +511     0xAA
       Total size:                512
  ~~~

- Common pc have two ide controllers(channels), each controllers is connected to two drives, named master/slave.
   ~~~
   Processor
            |___ primary 
                        |__master
                        |__slave
            |___ secondary
                         |__master
                         |__slave
   ~~~

- IDE ,Integrated Device, is a naming convention designing ATA, ATAPi etc.
- ATA : may be PATA for parallel ata, SATA for serial ata wich replace pata.
- two ways to read/write into ata drives : PIO(using polling) and DMA(using irq 14/15).

** Refs IDE **
- http://forum.osdev.org/viewtopic.php?f=1&p=167798#p167798
- ATA Interface reference manual - Seagate.



## Commands Linux
~~~
  $ fdisk -l disk.img  : partition list
  $ fdisk disk.img     : create partition (n 1 ... w)
  $ lsblk
    NAME         MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
    mmcblk0      179:0    0 14.7G  0 disk
    |-mmcblk0p1  179:1    0   20M  0 part
    `-mmcblk0p2  179:2    0    2M  0 part
~~~

## FS
Read a file: Sequence diagram
~~~
   |
   '-- sys_open(fpath)
          |
          '-- get_free_fd():fd
          '-- fp->f_op = &ext2_file_ops
          '-- namei (fpath, mode, fp)
   '-- fp->f_op->mmap (fp,vm): alias generic_mmap()
        |
        '-- vm->start = kmalloc(fp->f_inode->i_size, GFP_KERNEL)
        '-- vm->end = vm->start + fp->f_inode->i_size;
   '-- buf = vm->start;
   '-- sys_read(fd,buf,count) 
        |
        '-- fp->f_op->read(fp, buf, count): alias ext2_read_file (fp, buf, count)       
                       |
                       '-- ext2_ide_read()
                             |
                             '-- ide_read(dev, lba, size, buf) : PIO read
  ~~~                                  
                                    
                 
                  


## Ext2
- Organisation du fs ext2  
![](/documentation/images/FS-Ext2.jpg)

- mount  
  struct super_block * do_mount(int dev);
  // permet de charger en mémoire le super-bloc du péripherique (bloc) specifié.
- Initialisation du systeme de fchiers  
  void mount_root(void);
  // permet d'initialiser le systeme de fchiers, en montant à sa racine les fchiers du peripherique
     bloc racine.
     
- Super block : is 1024 bytes in length, and is always located at the 1024th byte on the disk.
- Block size = 1024 << s_log_block_size. common block size 1kB, 2kB, 4kB.
- Nb of groups = s_blocks_count / s_blocks_per_group.
- Groups includes data blocks and inodes stored in adjacent tracks
- All block, groups and inodes are numbred starting from 1. 
  block 1 hold superblock, block 2 contains group descriptors, block 0 is NULL and not reprented on the disk.
- block group start at block (group_num-1) * s_blocks_per_group.
- Size of the block bitmap = (blocks_per_group/8)/block_size.
- the block bitmap, which is used to iden-tify the blocks that are used and free inside a group, must be stored in a single block.
- Find the group of a block:  group = (block_num-1)/ blocks_per_group + 1
  Then the block in that group is block_num - (group*blocks_per_group)
  by this way you can access block_bitmap.
- Size of the inode bitmap = (inodes_per_group/8)/block_size.
- Find the group of a inode:  group = (inode_num-1)/ inodes_per_group + 1
  Then the inode in that group is inode_num - (group*inodes_per_group)
  by this way you can access inode_bitmap.
- Inode Table : <bg_inode_table> hold the first block storing inode table.
  inodes_per_block = block_size/sizeof(inode)
  inode_table_blocks = s_inodes_per_group/inodes_per_block : inode table size in blocks
- mk2fs.ext reserve un inode pour chque 4096B 
- read a node via its <inum>
  group = (inum-1)/ inodes_per_group + 1
  inum_in_this_group = inum - (group*inodes_per_group)
  inodes_per_block = block_size/sizeof(inode)
- Root Inode : is the inode number 2.
- Inode : may represente file, directory, device, socket.
- Inode number: is not stored on disk, it is a index in inode_table.

** Some calcul**
~~~
block_size=1024
blocks_per_group=8192
=>size of block bitmap=1 block 
--
block_num: 7000  8192  9000
group      1     1     2
--
block_size=1024
inodes_per_group=8192
--
inode_num: 500  8192  9000
group      1     1     2
-- inode Table size
if:
 s_inodes_per_group=1624
 block_size=1024
 sizeof(i.>>£>.>>	/node)=128
then:
 inodes_per_block = 1024/128 = 8
 inode_table_size = s_inodes_per_group/inodes_per_block = 1624/8 = 203 blocks=====================+
~~~

/!\ always round up divisions.

** references ext2
- see ext2.h
- http://uranus.chrysocome.net/explore2fs/es2fs.htm
- http://www.nongnu.org/ext2-doc/ext2.html
- http://cs.smith.edu/~nhowe/262/oldlabs/ext2.html


