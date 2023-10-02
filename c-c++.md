# Tricks
----
## Calling convention
https://en.m.wikipedia.org/wiki/Calling_convention

| Platform| Return Value| Parameter Registers| more Parameters| Scratch Registers| Preserved Registers| CallList  | 
| ------- | ----------- | ------------------ | -------------- | ---------------- | ------------------ | --------- | 
| i386    | eax, edx    | none               | stack          | eax, ecx, edx    | ebx,esi,edi,ebp,esp| ebp       | 
| X86_64 	| rax, rdx	  |rdi,rsi,rdx,rcx,r8/9| stack 			    |rax,rdi,rsi,rdx,rcx,r8/11|rbx,rsp,rbp,r12/15| rbp  |
| ARM		  | r0, r1	    | r0-r3	             | stack			    | r0-r3, r12			 | r4-r14	            |           |

The called function is allowed to modify the arguments on the stack and the caller must not assume the stack 
parameters are preserved. The caller should clean up the stack.

## Shared Libraries
https://www.technovelty.org/linux/plt-and-got-the-key-to-code-sharing-and-dynamic-libraries.html

compile with PIC (position independent code)

    $ gcc -Wall -O1 -I./include  -fPIC -c a2.c -o a2.o
  
create the shared library 'libtest.so': so name must start with 'lib'

    $ gcc -Wall -O1 -I./include  -shared -fPIC a2.o -o libtest.so

use 'libtest.so' in linking : options -l and -L  

    $ gcc -Wall -O1 -I./include  -L/path/to/lib -ltest  a1.o -o a1
  
use it in runtime linking :  

    $ export LD_LIBRARY_PATH=/path/to/lib:$LD_LIBRARY_PATH
    $ ./a1
  
you can also  put the library in defaul locations (/lib, /usr/lib, /usr/local/lib) or use ldconfig. to see wich so libs used by a program 'a1'  

    $ ld a1
    libtest.so => /usr/local/test/libtest.so (0x40014000)
        
inside the shared library   

    $ nm libtest.so, objdump, readelf

  
## GDB 
-- Debug c/c++ as assembly
```
 (gdb) set disassemble-next-line on      // very usefull
 (gdb) b main
 (gdb) b elf_reader.c:45 if i==10        // break if condition
 (gdb) r
 (gdb) ni       // next instruction
 (gdb) si
 (gdb) info reg [r1 sp rax etc]  //use space between registers
 (gdb) disp/x $r0
 (gdb) x/x $r7+4   //access memory [r7+#4]
 (gdb) disas
 (gdb) disp/10i
```

-- TUI mode // very usefull but bugs on gnuroot-debian
```
 (gdb) layout asm
 (gdb) layout regs
```

### GDB for c++
-- Vtable
```
  (gdb) set print vtbl
  (gdb) info vtbl s  //Shape* s = new Rectangle(2,3); s->surface();
     vtable for 'Shape' @ 0x10758 (subobject @ 0x22008):
     [0]: 0x105e1 <Rectangle::surface()>
```
-- passing parameters to debugged program
```
   # gdb --args janin -p
```

## Objdump 
```
   # objdump -D -j .text jvm.o
   # objdump -s -j .rodata janin
   # objdump -d janin
```

## XXD : see hexdump         
```
  $ xxd  -s 0x4ec -l 20  test/a1
  -s : start at offset. -l :  length in bytes to output
```
  
## readelf 
```
  readelf -s a.o
```
   
## GCC
Options gcc
   * -save-temps : produce all intermediary files, .i, .s, .o and a.out
   * -fPIC : create a Position Independant Code. this help shared libraries to be loaded at any address,
      instead of fixe address.
   * -D : Use compile time macros. example: gcc -Wall -DMY_MACRO main.c -o mai
     ```
     // main.c
     int main(void) {
     #ifdef MY_MACRO
       printf("\n Macro defined \n");
     #endif
       int i = 9;
       ...}
     ```

Generate assemply from .c

    gcc -O2 -S -c test.c 

          
## Objcopy  
Objcopy allow to strip all the ELF headers off and generate a flat binary executable .bin.   
```
   objcopy -O binary init.elf init.bin 
```

## c++filt - Demangle C++ and Java symbols.
```
  # readelf -s ObjectRef.o
  ...
  1067: 00000001   140 FUNC    GLOBAL DEFAULT  156 _ZN9ObjectRefC1EtSs
  # c++filt _ZN9ObjectRefC1EtSs
  ObjectRef::ObjectRef(unsigned short, std::basic_string<char, std::allocator<char> >)
```

## autotools : autoconf, automake
Install tools
```
     $ apt-get install autotools-dev
     $ apt-get install autoconf
```
Steps :
   -- create Makfile.am , this is automake input 
   ```
     bin_PROGRAMS = foo
     foo_SOURCES = foo.c foo.h bar.c
   ```
   -- generate 'configure.ac' by autoscan, must be renamed
   ```
   $ autoscan
   ```
  -- modify it
  ```
    AM_INIT_AUTOMAKE([1.14 -Wall -Werror])
  ```
   -- generate Makefile.in
   ```
    $ automake
   ```
   -- generate configure script
   ```
    $ autoreconf -i
   ```
  -- generate  Makefiles
   ```
     $ ./configure --host=armhf --prefix=/usr/local
   ```
  -- end
   ```
    $ make && make install
   ```
     
## Notes C 
**Designated Inits**  
-- Struct   
   ```
   struct point p = { .y = yvalue, .x = xvalue };
   is equivalent to
   struct point p = { xvalue, yvalue };
   /!\this is not implemented in C++
   ```
-- Array      
   ```
   To specify an array index, write ‘[index] =’ before the element value.
   int a[6] = { [4] = 29, [2] = 15 };
   is equivalent to
   int a[6] = { 0, 0, 15, 0, 29, 0 };
   
   with range:
   int widths[] = { [0 ... 9] = 1, [10 ... 99] = 2, [100] = 3 };
   /!\this is not implemented in C++
   ```

-- that is part of C extensions  
   https://gcc.gnu.org/onlinedocs/gcc-4.1.0/gcc/C-Extensions.html#C-Extensions  
   most extensions are available in C++
   
## Pointers
A pointer is a variable witch contains the address of an other variable.
  - '&' gives the address of the variable
  - '*' gives the content of the object pointed by the pointer.

Example :
```
 int i = 1, j=2;
 int *p, *q;  i [1]          p [x]      q[x]     j[2]
              @100           @1000      @2000    @3000
 p=&i;        i [1]          p [100]
 j=*p;        i [1]          p [100]             j[1]
 i=p;         i [100]        p [100]
 *p=5;        i [5]          p [100]   
 q=p;                        p [100]    q[100]
 p++;                        p [104]  | p pointe to @104, because "int" size is 4 bytes.
```

- Pointers and Arrays  
  ```
  ptr = &my_array[0];   => is identical to:   ptr = my_array;
  ```
  because decaying is implicit in C : array == &array == &array[0]
  
## references
-- http://beej.us/guide/bgc/output/html/multipage/

## C++ 
C++ internals[Excellent]: http://www.avabodh.com/cxxin/cxx.html

### C++ to C translation
Example:
  ```
  class Point {
  public:
    int x, y;
    int setX(int a) { x = a;}
  }
  ```
Usage:
  ```
  Point point;
  point.setX(10);
  ```
The equivalent C code:
  ```
  struct Point {
    int x, y;
  };
  int Point_setX(Point *this, int a) {
    this->x = a;
  }
  ```
And the usage:
  ```
  Point point;
  Point_setX(&point, 10);
  ```
  
### Divers
-- Create new object
  ```
  Point p = new Point(3,4); // create object in the heap
  Point a(3,4); // created on the stack
  Point []arr = new Point[10];
  ```
-- Free
  ```
  delete p;
  delete[] arr;
  ```
  
-- Operareur de cast
   ```
   class Point {
     int x, y;
     operator int() { return x; }// "cast" point --> int
   ```
     
   we can cast Point to int 
   ```
   Point a(2,9);
   int n = int (a); //idem to n=(int)a, n=static_cast<int>(a)
   ```
   the cast is called implicitly if not explicitly forbiden

-- Costructeur de copie
  ```
  class Point {
     int x, y;
     Point (Point const& p) { x = p.x; y = p.y;}
  }
  Point a(5,6), b;
  b = a; // equivalent a : b.x = a.x; b.y = a.y;
  ```
-- Compiler  
g++
 
-- auto_ptr : deprecated since c++11. use unique_ptr and shared_ptr instead!  
   shared_ptr can be stored inside containers.  auto_ptr can't.  
   unique_ptr is really the direct auto_ptr replacement, it combines the best features of both   
   std::auto_ptr and boost::scoped_ptr.

-- Null pointer  
 NULL  
 nullptr  (c++11)  

-- extern "C"  
   extern "C" is a linkage specification which is used to call C functions in the Cpp source files.
   

### Three Cast : 
 ```
 char c;
 int a = static_cast<int>(c); // instead of a=(int)c style
 reinterpret_cast<char*>(unsigned char*) : and verse versa is portable.
 ```
 - static_cast : is the first cast you should attempt to use. It does implicit conversions between types (such as int to float, or pointer to void*)  
 - const_cast : can be used to remove or add const to a variable.  
 - dynamic_cast : is almost exclusively used for handling polymorphism. You can cast a pointer or reference to any polymorphic type to any other class type.  
 - reinterpret_cast : is the most dangerous cast, and should be used very sparingly. It turns one type directly into another.  
 
### Reference : juste un alias de variable. 
 ```
  int a;
  int& ref_a = a; //doit etre initialisé au moment de sa delaration
  * les reference sont utiles pour le passage de parametres de fonction
  void f_inc(int& n)
  { n = n + 1;}
  int i = 8;
  f_inc(i); // va bien modifier i=9
  ```  
  - Les parametres de fonction doit etre passés par references[func(T& t)] pour tout objet de  taille superieur à 4, 
    afin d'eviter des copies de valeur suf la pile. Pour les types char,short et int on peut les passer en valeur[func(char c)]
    
### Output formating
- <iostream> //cout, cin  
- <iomanip> // setw  
- cout<<left<<setw(4)<<hex<<showbase<<opCode<<setw(15)<<instr.mnemonic<<endl;  
- setw(15) : say use 15 char for the next string  
- hex/dec : hexa or decimal format  
- showbase : to show 0x  

### STL : stlibc++. Standard Template Librairy.

-- Containers: vector, list(linked), set, map, stack, queue, 
 ```
 ***** vector : dynamic array, the elements are stored contiguously.
		|_ vector<T> v
		|_ vector<string> vect; vect.reserve(10); vect.push_back("aaa"); vect[5]="mmm"; 
		|_ (c++11) : T* datas = vect.data();
 ```
-- String : string, bitset  
-- iterator  
-- algorithm : find, count, sort, search elements in container  
-- auto_ptr : manage ptr to void mem leak  

### Polymorphism : 
- the method must be declared VIRTUAL,  
- or declared PURE VIRTUAL like : virtual int area() = 0;  
- the compiler will use the VTABLE to link the method call to the correct one  
 ```
   class Shape {
    public:
      virtual int area()
      {
         cout << "Parent class area :" <<endl;
         return 0;
      }
  };
  class Rectangle: public Shape{
   public:
      int area ()
      { 
         cout << "Rectangle class area :" <<endl;
         return 0;
      }
   };
 class Triangle: public Shape{
   public:
      int area ()
      { 
         cout << "Triangle class area :" <<endl;
         return 0; 
      }
  };
  ```
  main :
 ```
   Shape *shape;
   Rectangle rectangle(10,7);
   Triangle  triangle(10,5);

   shape = &rectangle;
   shape->area(); //will calculate rectangle area

   shape = &triangle; 
   shape->area();//will calculate triangle area
 ```
 
### Function overloading 
 Function overloading allows us to create multiple functions with the same name, 
 so long as they have different PARAMETERS.
 
    int add(int x, int y); 
    double add(double x, double y); //OK, because differents parameters

    int getRandomValue();
    double getRandomValue(); // compiler error, same parameter(void)
 
- "does not name a type" error  
the compiler must know the type size. to resolve this problem:  
 * define the class before using it
 * or declare class "class MyClass;" and use pointer "MyClass* toto;"

-- Docs  
- Programmation en C++ : cours de Berthran Cottenceau sur le net.  
- http://www.yolinux.com/TUTORIALS/LinuxTutorialC++STL.html  
- http://en.cppreference.com/w/  
- Reverse engineering http://danielebellavista.blogspot.com/2014/10/reversing-c-binaries-2-objects.html  


## Biblio standards C/C++ 
- en C++, la declaration <clib> remplace <lib.h> pour les librairies standards C.  
- <cstdio>(stdio.h) : printf,
- iostream : cin, cout, remplace stdio.
- fstream : ifstream, ofstream, open files 
- <cstdlib>(stdlib.h) : malloc, exit, EXIT_FAILURE
- <cassert>(assert.h) : assert(x == 7)
- stddef.h : offsetof 
   
## Regles de code C 
http://lxr.free-electrons.com/source/Documentation/CodingStyle

- Accolades : 
  ```
   func
   {
   }
   if () {
   }
  ```
- Operateurs : laisser un espace les oprandes et l'operateur
  ```
   prot += PAGE_RW
   sauf pour i=0 et j=0 dans for
  ```

- Espaces
  ```
   for (i=0; i < PAGE_NB(0x400000); i++) {
   }

  if (x == y) {                ..
  } else {
     ....
  }
  ```
--- Do not add spaces around (inside) parenthesized expressions.
  ```
   s = sizeof( struct file ); /*bad*/
   s = sizeof(struct file); /*good*/   
  ```
--- '*' is adjacent to the data name or function name and not adjacent to the type name.  Examples:
  ```
   char *linux_banner;
   char *match_strdup(substring_t *s);
  ```
---  Use one space around (on each side of) most binary and ternary operators:
     =  +  -  <  >  *  /  %  |  &  ^  <=  >=  ==  !=  ?  :
  ```
     Ex. x = 3 + i;
     but no space after unary operators:
         &  *  +  -  ~  !  sizeof  typeof  alignof  __attribute__  defined
      Ex. x = ~(1 << 8);
  ```
  
-- Align switch and its cases
  ```
   switch (suffix) {
   case 'a':
           break;
   case 'b':
           mem <<= 30;
           break;	
   default:
          break;
   }
  ```


-- Comments
Use C89 style 
  ```
  /* ... */
  
  /*
   * 
   */
  ```
Dont use C99 style : //...

-- Macros  
---- must enclose the expression in parentheses.  
  ```
   #define SIZE 0x4000
   #define CEXP (SIZE << 4)
  ```

## Reverse engineering C++
### Example  
// Compile
//   g++ -Wall file.cpp -o file.bin  
// Disassable  
//   objdump -d file.cpp  
// Source : http://danielebellavista.blogspot.com/2014/10/reversing-c-binaries-2-objects.html  
// ARMv7 assembler  

```
class TestClass
{
  public:
  // _ZN9TestClassC1Ev
  // params : r0 = @this
  TestClass()
  {
    x = 5;          // add	r7, sp, #0
	y = 7;		  // str	r0, [r7, #4]   <-- r0 = @this, passed by param in r0
					// ldr	r3, [r7, #4]   <-- r3 = @this.x, offset=0
   		   	  // movs   r2, #5
  				  // str	r2, [r3, #0]   <-- this.x = 5
   				 // ldr	r3, [r7, #4]   <-- r3 = @this.y, offset = 4
   				 // movs   r2, #7
   				 // str	r2, [r3, #4]  <-- this.y = 7
    stuff = 9;
  }

  // _ZN9TestClassD1Ev
  // params : r0 = @this
  ~TestClass()
  {
    stuff = 0;
  }

  // _ZN9TestClass8GetStuffEv
  // params : r0 = @this
  // return : in r0
  int GetStuff()
  {
    return stuff; 	// push	{r7}
      				// sub	sp, #12
         			 // add	r7, sp, #0
        			  // str	r0, [r7, #4]
         			 // ldr	r3, [r7, #4]	; r3 = @this
        			  // ldr	r3, [r3, #8]    ; r3 = this.stuff, stuff-ofsset=8
       			   // mov	r0, r3		  ; resultat in r0
        			  // adds   r7, #12
         			 // mov	sp, r7
    				  // ldr.w  r7, [sp], #4
        			  // bx	 lr			  ; branch to link register(return address)

  }

  private:
  int x;
  int y;
  int stuff;
};
```

//-- Local Objects  
//   The following function initialize a class onto the stack and calls the method GetStuff:  
// _Z7OnStackv  
```
int OnStack()
{
  TestClass t1;
  return t1.GetStuff();
  /*105ac:	b590         push	{r4, r7, lr}
   105ae:	b085      	sub	sp, #20
   105b0:	af00      	add	r7, sp, #0
   105b2:	1d3b      	adds   r3, r7, #4
   105b4:	4618      	mov	r0, r3  	;r0 = @t1 = sp+4
   105b6:	f000 f88d 	bl	 106d4 <_ZN9TestClassC1Ev>
   105ba:	1d3b      	adds   r3, r7, #4
   105bc:	4618      	mov	r0, r3      ; r0 = @t1
   105be:	f000 f8ab 	bl	 10718 <_ZN9TestClass8GetStuffEv>
   105c2:	4604      	mov	r4, r0
   105c4:	1d3b      	adds   r3, r7, #4
   105c6:	4618      	mov	r0, r3     ; r0 = @t1
   105c8:	f000 f898 	bl	 106fc <_ZN9TestClassD1Ev>
   105cc:	4623      	mov	r3, r4
   105ce:	4618      	mov	r0, r3
   105d0:	3714      	adds   r7, #20
   105d2:	46bd      	mov	sp, r7
   105d4:	bd90      	pop	{r4, r7, pc}   ; return by pop lr in pc!
   105d6:	bf00      	nop
  */
}
```


//-- Dynamic Allocated Object  
//   An heap based initialization implies the use of the new and delete operator which respectively trigger   
//   the class constructor and destructor. The new operator, which resides in a shared library, performs a malloc,    
//   while the delete operator performs a free.  
// _Z6OnHeapv  
```
int OnHeap()
{
  // new: _Znwj@plt
  // con: _ZN9TestClassC1Ev
  TestClass* t1 = new TestClass(); // movs	r0, #12                   // size to pass to malloc
                                   // blx	104b4 <_Znwj@plt>          // new
                                   // mov	r4, r0  				   // object pointer returned in r0
                                   // mov	r0, r4
                                   // bl	 106d4 <_ZN9TestClassC1Ev>  // constructor

  int ret = t1->GetStuff();

  // des: _ZN9TestClassD1Ev
  // delete: _ZdlPv@plt
  delete t1;
  return ret;
}
```

//-- Global Objects  
//   Both static and global objects are initialized before the main is called,  
//   by an initialization routine. The same routine saves the new references and  
//   the destructor address into a global table, where they will be destroyed by  
//   the __run_exit_handlers routine, executed after the main function.  
```
TestClass tg;
static TestClass ts;

int GlobalTc()
{
  return tg.GetStuff() + ts.GetStuff();
}

int main()
{
  OnStack();
  
  OnHeap();
  
  GlobalTc();
}
```





   
   
