---
layout: default
title: Ansible Tower
parent:  Ansible
grand_parent: DevOps
nav_order: 5
---

<h1>UNDER CONSTRUCTION!</h1>

### Getting Started
**Ansible Tower** knwon as Red Hat **Ansible Automation Platform** is a console interface for Ansible.

### Concepts
- **Project**: collections of ansible playbooks. they can reside localy on the tower server, or on vesion control supported by tower(eg. git).

- **Inventory**: collection of hosts against wich jobs may be launched. it's the same as traditional ansible inventory.

- **Credentials**: used by tower to authenticate when launching jobs against machines, to import projects from version control servers,

- **Templates**: parametrable jobs.

- **Jobs**: A job is basically an instance of Tower launching an Ansible playbook against an inventory of hosts.


### Inventories
![to](/docs/images/ansible-tower-inventory-1.png)
![to](/docs/images/ansible-tower-inventory-2.png)


### Credentials
- CREDENTIAL TYPE: Click on the magnifying glass, pick Machine. 
- PRIVILEGE ESCALATION METHOD: sudo
![to](/docs/images/ansible-tower-credentials.png)

### Create a Project
- SCM URL: https://github.com/ansible/workshop-examples.git
![to](/docs/images/ansible-tower-projects.png)

### Create a Job Template and Run a Job
- CREATE JOB TEMPLATE
  - Name: Install Apache
  - INVENTORY: preprod
  - PROJECT: Ansible Workshop Examples
  - PLAYBOOK: apache_install.yml
![to](/docs/images/ansible-tower-template.png)


### Trial Download
<a>http://www.ansible.com/tower-trial</a>

### Installation
~~~sh
curl --insecure -o "/opt/ansible-tower-setup-latest.tar.gz" "https://releases.ansible.com/ansible-tower/setup/ansible-tower-setup-latest.tar.gz"
~~~

Edit the inventory file, and define passwords.

~~~sh
cd /opt/ansible-tower-setup-3.8.6-2/
./setup.sh
~~~

{: .important }
> Error: This machine does not have sufficient RAM to run Ansible Tower/Automation Hub.
>
> Solution: Edit  **ansible-tower-setup-3.8.6-2/roles/preflight/defaults/main.yml**: 
>    required_ram: 1024

If install OK, **/etc/ansible** and **/etc/tower** are created.

Ckeck service:
~~~sh
ansible-tower-service status
~~~

### Use Tower
Start/Stop 
~~~sh
ansible-tower-service restart
~~~
Console: https://<TOWER_SERVER_NAME>/
- admin/changeit

Config: 
- /etc/tower/conf.d/

### Error logs
- **/var/log/tower**
- Nginx logs are http logs
- can be configured in /etc/tower/conf.d/ 

### Unable to login to Tower via HTTP
Error : ERR_SSL_KEY_USAGE_INCOMPATIBLE

See: https://access.redhat.com/solutions/6955072

See: https://docs.ansible.com/ansible-tower/latest/html/administration/troubleshooting.html#error-logs

### Docs
- Excellent Ansible Workshops: https://redhatgov.io/workshops/ansible_automation
- https://goetzrieger.github.io/ansible-tower-getting-started
- https://www.freekb.net/Articles?tag=Ansible
- https://docs.ansible.com/ansible-tower/