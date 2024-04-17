---
layout: default
title: Yaml Syntax
parent:  Ansible
grand_parent: DevOps
nav_order: 15
---

### List
~~~yaml
---
- Car
- Train
- Moto
~~~


### Dictionary
A dictionary is represented in a simple key: value form (the colon must be followed by a space):
~~~yaml
---
casablance:
  country: morocco
  population: 3.359.818
  constructed: 1756
  postal_code: 20000-20200
~~~


### Data Structures 
mix of list and dictionnaries
~~~yaml
---
- casablance:
    country: morocco
    population: 3.359.818
    constructed: 1756
    postal_code: 20000-20200

- ElJadida:
    country: morocco
    population: 220.181
    constructed: 16th century
    postal_code: 240x0
~~~

Dictionaries and lists can also be represented in an abbreviated form if you really want to:
{% raw %}
~~~yaml

---
file:  path={{ __logs_dir }} state=directory mode=0755

martin: {name: Martin D'vloper, job: Developer, skill: Elite}

fruits: ['Apple', 'Orange', 'Strawberry', 'Mango']

~~~
{% endraw %}


### Multiple Lines Values
Values can span multiple lines using `|` or `>`
~~~yaml
---
# An employee record
name: Ali Ben
job: Ingeneer
employed: True
languages:
  perl: Elite
  python: Elite
  pascal: Lame
education: |
  4 GCSEs
  3 A-Levels
  BSc in the Internet of Things
~~~

### Gotchas
To be able to put special caracters(`:`, `{}`, `|` etc) in a value, you can surrount with with `'` or `"`
~~~yaml
---
# Error
url: http://example.com

# Correct
url: 'http://example.com'

~~~



### List
~~~yaml
~~~