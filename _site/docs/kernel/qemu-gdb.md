
## QEMU & GDB Info

- Notes importantes

   - It is recommanded to install qemu package, rather than building from sources.  

     apt install qemu  

   - to debug real mode : 
     > 'set arch i386' in gdb
   
   - breakpoints dont work properly if  base address(in GDT) is not 0x0(see head.S). You can do 'break *0xc0001234' but...
   
       
- Build Qemu  from sources
  > ./tools/build-qemu.sh
  
- Compiler avec "-g" , puis generer .bin a partir .elf(voir le Makefile):
  > objcopy -O binary  kernel.elf kernel.bin

- Qemu Monitor commands : https://www.qemu.org/docs/master/system/monitor.html


## Qemu Monitor
- Access Qemu Monitor :  
         
    >Qemu 4: Ctr-a c  
    >Qemu 2 graphical : Ctl+Alt+1 ou 2.  
    >Qemu 2 : Esc+2 and Esc+1 au lieu de Ctl+Alt+1 ou 2.  
    >Qemu 2 : Liberate mouse Ctl+Alt
   

- Exit Qemu:

    > For Qemu4 : Ctrl-a x  
    or  
    > (qemu) q

- Scroll  

    > Ctrl+PgUp/PgDown

- Monitor 

    > info registers
    > info pci


## Debug Qemu with  GQB

**GDB freindly output:**
  - To debug real mode code, [set architecture i8086]
    > cp tools/gdbinit_real_mode.txt ~/.gdbinit
  - To debug C code
    > cp tools/gdbinit_c.txt ~/.gdbinit  

  - To debug ASM code/protected mode
    > cp tools/gdbinit_asm.txt ~/.gdbinit


**Debugging protected mode** 
  ~~~
  $ cp ~/magOS/tools/gdbinit_asm.txt ~/.gdbinit
  $ edit ~/magOS/tools/gdb.cmd 

  $ ~/magOS/Labs/run-qemu-Lab.sh 3 -g

  $ gdb -x ~/magOS/tools/gdb.cmd 
  ~~~


**Run Qemu in debug mode**:

> ./qemu-system-i386 -s -S /logiciels/floppyA.img -no-fd-bootchk 

-s equivalent a gdb tcp::1234



**Run GDB**:
- Run commands from a file for user/kernel Spaces
  > gdb -x ~/magOS/tools/gdb.cmd

~~~
 $ gdb
  (gdb) target remote localhost:1234
  (gdb) set architecture i8086     #only to debug real mode code
  (gdb) symbol-file kernel.elf
       b init_gdt
       b *0x1000
       b main.c:63
       b *0xC0001234     - ne fois active la pagination (PAGE_OFFSET=0xC0000000), sinon qemu ne break pas
       info breakpoints
       advance *0x1046   - advance execute to adr/label
       n
       ni   - next asm instr
       si   - step in 
       x/Nx addr  - Dump in hex N words starting at virtual address addr. 
       x/Ni addr  - display N intr assembler
       xp/Nx paddr  - physical addr
       x/x $eip
       x/10i $eip  - dump 10 asm instruct from current eip(Useful)
       x/10i 0x90000
       disas  $eip,+100   - disassemble 100 instruction at eip
       x/5x $esp   - inspecter la pile 
       x/x &pgt0   - si "x/x pgt" ne montre rien
       disas       - show current asm instrs
       info symbol  swapper_pg_dir      - essayer &
       info symbol  &swapper_pg_dir
       x/10x &swapper_pg_dir
       list
       info reg      //dump all registers
       info reg esp
       info mem
       info pg
       where ou bt(backtrace)
       display 	  	- affiche la valeur d'une expression à chaque arrêt du programme
       undisplay
~~~

**Debug real mode**
~~~
  /!\ apres la command "cont" if faut faire  "delete", afin de supprimer le breakpoint
      car gdb se bloque et "ni" ne le fait plus avancer!!!. apres on peut creer un new break, mais il
      faut le supprimer aussi apres "cont".
   (gdb) set architecture i8086     #only to debug real mode code
   (gdb) b *0x7c00
         hb *0x90219   //hard break, if softbreak dont work
         x/10i $cs*16+$eip   //to dump the code at the PC position.
         ni   - next asm instr
         si   - step in 
         stepo  - step out an int or a function call
       
~~~


**Qemu Monitor** : to watch machine registers, etc
~~~ 
Ctrl-a c , or Ctrl+Alt 2 et 1, Or Esc+2: To access qemu monitor.
 
(qemu) info registers       # show machine regs: GDT, CR0, CS, etc
(qemu) info mem     # paging info  
       info irq      
       info pic
 ~~~

 
- Access au registers GDTR,CR0,.... 
     > Depuis la console Qemu, tapper "info registers"


- Objcopy :  is part of the GNU binutils package  
    ~~~
    $ objcopy --only-keep-debug kernel.elf kernel.sym  
    $ objcopy --strip-debug kernel.elf  
    $ objcopy -O binary kernel.elf kernel.bin  
  
    (gdb) symbol-file kernel.elf     
    ~~~
- chercher une aide par keyword
  > (gdb) apropos myword

- Call a function in gdb
  ~~~
    gdb$ p/x *find_task(1)
    we can also do:
    gdb$ call find_task(1)
    $1 = (task_t *) 0xc1fdb000
    gdb$ p *$1
  ~~~

- make gdb save history

    Create a file $HOME/.gdbinit with the following content:
    >set history save
    
- Quit without confirm prompt
  ~~~
    $ nano ~/.gdbinit with:
      define hook-quit
      set confirm off
      end
  ~~~

- gdb; passe argument to programm
  > gdb --args progfile arg1 arg2

## Debug with GDB and GDB Server
  run gdbserver: 
    > $ gdbserver [localhost]:1234 mm_test.bin
  
  run gdb:
  ~~~
    $ gdb --directory=/path/to/src /usr/magOS/bin/test/mm_test.bin
      (gdb) target remote localhost:1234
      (gdb) b main
      (gdb) c
  ~~~
  
  you can use this:
  > $ gdb --directory=/magOS/mm /magOS/bin/test/mm_test.bin -ex="target remote localhost:1234"


## Refs  
- http://wiki.osdev.org/Kernel_Debugging  
- https://qemu.weilnetz.de/doc/qemu-doc.html  
- https://en.wikipedia.org/wiki/QEMU#Emulated_hardware_platforms

