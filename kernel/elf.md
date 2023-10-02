

## ELF Format
http://geezer.osdevbrasil.net/osd/exec/elf.txt   
https://docs.oracle.com/cd/E19683-01/816-1386/6m7qcoblj/index.html#chapter6-73709  
http://man7.org/linux/man-pages/man5/elf.5.html  
http://wiki.osdev.org/ELF_Tutorial  

```
     ELF layout
   ------------------          
  | ELF Header       |   - In linking view, program header table is optional     
  |------------------|   - In executiom view, section header table is optional
  | Program header   |   
  | table            |   - A program segment may hold many section having same flags
  |------------------|   - Sections contain all information in an object file except the ELF header,  
  | section 1        |     the program header table, and the section header table.
  |------------------|
  | ...              |
  |------------------|
  | section n        |
  |------------------|
  | section name     |
  | string table     |
  |------------------| 
  | section header   |
  | table            | 
   ------------------
```

- An ELF file's program header table contains one or more PT_LOAD
  segments, which corresponds to portions of the file that need to
  be mapped into the process' address space.

- **Relocation**  
  Relocation is the process of connecting symbolic references with symbolic definitions. For example, 
  when a program calls a function, the associated call instruction must transfer control to the proper destination 
  address at execution.
```  
  typedef struct {
      Elf32_Addr      r_offset;      /* Location to be relocated. */
      Elf32_Word      r_info;        /* Relocation type and symbol index. */
  } Elf32_Rel;

  #define ELF32_R_SYM(info)      ((info) >> 8)           /*symbol index*/
  #define ELF32_R_TYPE(info)     ((unsigned char)(info)) /*type : OBJECT, FUNC,...*/
  r_offset:
    For a relocatable file, the value indicates a section offset.
    For an executable or shared object, the value indicates the virtual address of the storage unit 
    affected by the relocation. useful for runtime linker.
```

- **PLT** - Procedure Linkage Table : Section .plt  
    used to call external procedures/functions whose address isn't known in the time of   
    linking, and is left to be resolved by the dynamic linker at run time.  
- **GOT** - Global Offsets Table  : Section .got  
    used to resolve addresses for global and static variables.

- **Symbol Table**  
 symbol table holds information needed to locate and relocate a program's symbolic definitions and references. 
```
 typedef struct {
      Elf32_Word      st_name;      /* String table index of name. 
      Elf32_Addr      st_value;     /* Symbol value. */
      Elf32_Word      st_size;      /* Size of associated object. */
      unsigned char   st_info;      /* Type and binding information. */
      unsigned char   st_other;     /* Reserved (not used). */
      Elf32_Half      st_shndx;     /* Section index of symbol. */
  } Elf32_Sym;

```
#### Understand relocations
https://www.technovelty.org/linux/plt-and-got-the-key-to-code-sharing-and-dynamic-libraries.html  
http://eli.thegreenplace.net/2011/08/25/load-time-relocation-of-shared-libraries

- a2.c : libtest.so
```
    int my_glob = 7;
    
    int ml_func (int n) 
    {
      my_glob += n;
      return my_glob;
    }
```
 
- a1.c : this uses libtest.so. see above to compile and use shared libs.
```
    extern int my_glob;
    extern int ml_func(int);
    int main () 
    {
      ml_func (3);
      printf ("my_glob = %d\n", my_glob);
      return 0;
     }
```
- Entry point of libtest.so
```
 $ readelf -h libtest.so
 ELF Header:
  ...
  Machine:                           ARM
  Entry point address:               0x424
```

- Disassemble : focus on function ml_func
```
 $ objdump -d -j .text libtest.so
 00000518 <ml_func>:
 518:   4b03            ldr     r3, [pc, #12]   ; (528 <ml_func+0x10>)
 51a:   447b            add     r3, pc
 51c:   4a03            ldr     r2, [pc, #12]   ; (52c <ml_func+0x14>)
 51e:   589a            ldr     r2, [r3, r2]    ; r2 = @my_glob = [0x1010a + 0x20]
 520:   6813            ldr     r3, [r2, #0]    ; r3 = [my_glob]=7
 522:   4418            add     r0, r3          ; r0 = n + 7
 524:   6010            str     r0, [r2, #0]    ; [my_glob]=r0
 526:   4770            bx      lr
 528:   0001010a        .word   0x0001010a
 52c:   00000020        .word   0x00000020
 
 $ objdump -d -j .text a1.o
 00000000 <main>:
   0:   b510            push    {r4, lr}
   2:   4c07            ldr     r4, [pc, #28]   ; (20 <main+0x20>)   4: 447c  add r4, pc
   6:   2003            movs    r0, #3
   8:   f7ff fffe       bl      0 <ml_func>
   c:   4b05            ldr     r3, [pc, #20]   ; (24 <main+0x24>)   e: 58e3  ldr  r3, [r4, r3]
  10:   4805            ldr     r0, [pc, #20]   ; (28 <main+0x28>)  12: 4478  add  r0, pc
  14:   6819            ldr     r1, [r3, #0]
  16:   f7ff fffe       bl      0 <printf>
  1a:   2000            movs    r0, #0
  1c:   bd10            pop     {r4, pc}
  1e:   bf00            nop
  20:   00000018        .word   0x00000018
  24:   00000000        .word   0x00000000
  28:   00000012        .word   0x00000012
``` 

- relocations
```
   $ readelf -r libtest.so
   Relocation section '.rel.dyn' at offset 0x394 contains 9 entries:
   Offset     Info    Type            Sym.Value  Sym. Name
   ....
   00010648  00000c15 R_ARM_GLOB_DAT    00010658   my_glob
```  
 