## BIOS

**Interrupts list**  
    https://stanislavs.org/helppc/int_table.html

**Important Interrupts**
    * INT 10,0 - Set Video Mode
    * INT 0x10 : Video display functions (including VESA/VBE)
    * INT 0x13 : mass storage (disk, floppy) access
    * INT 0x15 : memory size functions
    * INT 0x16 : keyboard functions 

**INT 10,0**: Set Video Mode
  ~~~
  AH = 00 : set video mode function
  AL = 03  80x25 16 color text (CGA,EGA,MCGA,VGA)
     = 12  640x480 16 color graphics (VGA)
     ...
  ~~~

**INT 0x13** : mass storage (disk, floppy) access
  * Function 0x2 : to read sectors from disk into memory  
    ~~~
    Call with   %ah = 0x2 : read function  
                %al = number of sectors  
                %ch = cylinder  
                %cl = sector (bits 6-7 are high bits of "cylinder")  
                %dh = head  
                %dl = drive (0x80 for hard disk, 0x0 for floppy disk)  
                %es:%bx = segment:offset of buffer  
     Return:  
                %al = 0x0 on success; err code on failure  
    ~~~

**INT 10H** : Video display functions (including VESA/VBE)  
  AH register contains the function number
  * Function 0Eh : Write Text in Teletype Mode  
      ~~~
      %ah = 0xe : function write    
      %al = ASCII character to write  
      %bh = page        
      %bl = foreground color (graphics modes)  
      ~~~

  * Erase Screen
      ~~~
      mov $0x03, ax
      int $0x10
      ~~~
    


      