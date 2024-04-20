---
layout: default
title: Conditionals
parent:  Ansible
grand_parent: DevOps
nav_order: 3
---

## Test with **when**
Test Syntax:
~~~yaml
- name: TASK
  ...
  when: condition
~~~ 

is equivalent to: 
~~~ c
if (condition) 
  { execute TASK }
~~~
If `condition` is not met, the `TASK` will be skipped.

### Test based on ansible_facts
{% raw %}
~~~yaml
- name: Show facts available on the system
  debug:
    var: ansible_facts  

- name: Message if Ubuntu installed
  debug:
    msg: "Your OS version is {{ ansible_facts['distribution'] }}  {{ansible_facts['distribution_version'] }}"
  when: ansible_facts['distribution'] == "Ubuntu" and 
        ansible_facts['distribution_major_version'] == "22"
~~~
{% endraw %}

### Test on Registered Variable
~~~yaml
- name: Register a variable
  shell: cat /etc/os-release
  register: os_release_contents

- name: Test on registered variable
  debug:
    msg: os-release contains the word Ubuntu
  when: os_release_contents.stdout.find('Ubuntu') != -1
~~~

Check for Emptiness:
~~~yaml
- name: List contents of directory
  command: ls mydir
  register: contents
  ignore_errors: true

- name: Check contents for emptiness
  debug:
    msg: "Directory is empty or not exist"
  when: contents.stdout == ""
~~~

Test with `when: registered_var is succeeded`. In the example below, the task containing `when` condition will be executed only if the task that registred `result` was `succeeded`.

~~~yaml
  - name: Register a variable, ignore errors and continue
    command: ls -l
    register: result
    ignore_errors:
	
	- name: Run only if the task that registered the "result" variable succeeds
     command: /bin/something
     when: result is succeeded
~~~
Other possible conditions : `failed`, `changed`, `skipped`

### Test based on variables
~~~yaml
vars:
  - foo: 'fou'

- name: Run the command if "foo" is defined
  debug:
    msg: "I've got '{{ foo }}' and am not afraid to use it!"
  when: foo is defined

- name: Fail if "bar" is undefined
  fail: msg="Bailing out. This play requires 'bar'"
  when: bar is undefined
~~~



