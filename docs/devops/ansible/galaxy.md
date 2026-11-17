---
layout: default
title: Ansible Galaxy - Collections
parent:  Ansible
grand_parent: DevOps
nav_order: 4
---


### Reutiliser un role depuis le Repo Galaxy
- Exemple : le role geerlingguy.docker. 
~~~
ansible-galaxy install -r requirements.yml
~~~

requirements.yml
~~~
---
roles:
  - name: geerlingguy.docker
    src: geerlingguy.docker
    version: "7.4.7"
~~~

- L'utiliser dans votre playbook comme n'impote quel autre rol


### Collections
Collections are a distribution format for Ansible content that can include playbooks, roles, modules, and plugins. You can install and use collections through a distribution server, such as Ansible Galaxy.

[Ansible galaxy](https://galaxy.ansible.com/) is a popular distribution server where the ansible collections are hosted.

### Install a Collection Localy
**Syntax**
~~~sh
ansible-galaxy collection install namespace.collection
~~~

Example
~~~sh
ansible-galaxy collection install middleware_automation.wildfly
~~~

Collection are installed in:
~~~
$HOME/.ansible/collections/ansible_collections
~~~

