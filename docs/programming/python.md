---
layout: default
title: Python
parent: Programming
nav_order: 10
---
### Lists
~~~py
animals = ["lion", "vache", "mouton", "souris"]
for animal in animals:
  if animal == 'lion': 
    print(f"- The {animal} is the king!")
  else:
    print(f"- {animal} --->")
~~~

### Dictionary
Dictionary syntax: `dict_var = {key1 : value1, key2 : value2, …..}`

~~~py
employee1 = {'name': 'Hossein', 'email': 'hosseil@gmail.com'}

print("Employee:", employee1['name'])
~~~

### Create a Module
a module is file with `.py` extension, containing python definitions and statements. the module name is same as file name.

Create a Module `greeting.py`:
~~~py
def sayHello(name):
	print ("Hello", name)

class Person:

	def __init__ (self, name):
		self.name = name
	
	def salute (self):
		print ("Salutation", self.name, "!")
~~~

Use the `greeting` module in `testModule.py`:
~~~py
import greeting

greeting.sayHello("Marcello")

person = greeting.Person("Gonzalo")

person.salute()
~~~