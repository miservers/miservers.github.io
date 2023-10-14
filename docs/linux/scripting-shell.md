---
layout: default
title: Scripting Shell
parent: Linux
nav_order: 1.5
---

Envrionment: Bash

### Select
Create *select.sh*: 

```sh
  #!/bin/bash

  PS3='Choose one word: ' 
  
  select word in "linux" "bash" "scripting" "tutorial" 
  do
    echo "The word you have selected is: $word"
    # Break, otherwise endless loop
    break
  done
```

Run it :

```sh
  $ ./select.sh
    1) linux
    2) bash
    3) scripting
    4) tutorial
    Choose one word: 2
    The word you have selected is: bash
```

### Case
```sh
  read var;
  case $var in
    1) echo "You selected bash";;
    2) echo "You selected perl";;
    3) echo "You selected phyton";;
    4) echo "You selected c++";;
    5) exit
  esac
```

 OS select:
```sh
case $os in
     SunOS*) PS="/usr/ucb/ps auxww";;
     Linux*) PS="ps -ef";;
esac
```

### Arithmetic expressions
```sh
  formats  $[ expression ]  and $(( expression ))
  
  k=`expr 1900 + 1024`
  k=$(( 5 + 3 ))
  k=$[ 5 + 3 ]
  /!\ : no space around '=', but one space afer [ , (( and +.
```

### Expr

    PROC_NR=$(ps -ef|grep java| grep -v  |wc -l)

### Substitution temporaire

    ${var-$sub} : vaut var si var existe, sub sinon
    ${var:-$sub}: vaut var si var est non vide, sub sinon

    
### Copy dir to dir

    cd /from/mydir
    tar cf - . | (cd /to/bkp/mydir && tar xfp -)

  
### Special chars

    [[]], [] : test. [[]] more flexible than []
    - : current dir. "cd -" 

- http://tldp.org/LDP/abs/html/special-chars.html 


### test 
same as placing the EXPRESSION between [].  

    test $a -gt $b && echo "Yes, a>b." || echo "No, a<=b."

	this will return "Yes, a>b." 

### IF

Syntax

	if <condition>; then 
		<commands> 
	elif <condition>
	then
		<commands> 
	else
		<commands> 
	fi

Table of conditions (Some):

**Files** : [ -a existingFile ], [ -d directory ], [ -h symboliclink ], [ -x executablefile ]

**String** : [ str1 == str2 ], [ str1 != str2 ]

**Arithmetic** : [ a -eq b ], [ a -ne b ]. Others Operators: -gt, -ge, -lt, -le 


Rules:
  1. keep space between the brackets and the check
		```sh
		if [$a < 9]; then    // Error
		if [ $a < 9 ]; then  // Correct
		```

  1. shell keywords like if, then, fi, else, for, etc cannot share the same line. 
	Terminate the line before putting a new keyword or put a ";" between the keywords.
		```sh
		if [ ... ] then ... fi // Error

		if [ ... ]; then ...
		fi                     // Ok

		if [ ... ]
		then
		fi                     // OK                 
		```

**Double Brackets [[...]]**

Double brackets serve as enhanced version of single brackets. here some differences

- Asterisk(*) will expand anything

	```sh
	if [[ "$var" == *[eE]ssalam* ]]  // essalama, Essalam,... match the condition
	```

- Combining conditions

	```sh
	if [[ $a -eq 6 && "$str" == bar ]]   //OK
	```

	```sh
	if [ $a -eq 6 && "$str" == bar ]  // BAD .  may have error missing `]'
	```

**Double-parenthesis ((...))**

used for arithmetic conditions, with 'normal' operators (<, >, ==, <=, &&, ||) 

```sh
if (( $var <= 5 && $a == 9 )); then
``` 
	  
### Check file

```sh
[[ ! -f "$filename" ]] && { echo "ERROR :  file not exists!";
                        echo ""  
                        exit 1;
                    }
                    
[[ ! -r "$filename" ]] && { echo "ERROR :  access denied!";
                        echo ""
                        exit 1;
                    }
``` 

### Parameters parsing

```sh
while [ "$1" != "" ]; do
	case $1 in
		-r | --read ) shift
					  filename=$1
					  read $filename
					  ;;
		-h | --help )  usage
					   exit
					   ;;
		-x | --debug ) set -x
					   ;;
		* )            usage
					   exit 1
	esac
	shift
done
``` 


