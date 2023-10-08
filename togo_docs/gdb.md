## GDB
This usecase apply to C/C++ programs.

**Important** : the code must be compiled with `-g` debug flag.

```c
$ gdb path/to/myProgram
(gdb) b main    // break in main
(gdb) b MyClass::myMethod  // use keyboard TAB for completion
(gdb) r         //run, start the program
(gdb) n         // next instruction
(gdb) s         // step into the function call
(gdb) p my_var  // print var/exp values
(gdb) x 0x8407 
(gdb) x &temp   // examine memory at address
(gdb) info b    // list of breakpoints
(gdb) c         // continue program execution
(gdb) l(ist)    // list by 10 lines of source code 

(gdb) set i=10*j  // charge value of var, memory, register

(gdb) backtrace   // display the call stack

(gdb) info locals   //display local vars
    i = 1431847300
    clazz = 0x555555584008
    class_file = "./test/Hello.class"
    opt_p = 0

(gdb) info args
    nargs = 1
    argv = 0x7fffffffdd78

(gdb) info b    // list of breakpoints
(gdb) delete 1  // delete breakpoint n1


(gdb) help info   // very important help about gdb commands

```

