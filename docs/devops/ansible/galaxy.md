---
layout: default
title: Ansible Galaxy - Collections
parent:  Ansible
grand_parent: DevOps
nav_order: 4
---
<h1>UNDER CONSTRUCTION !</h1>

## Ansible Galaxy


## Collections
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

