---
layout: default
title: Ansible Tower
parent:  Ansible
grand_parent: DevOps
nav_order: 5
---


### Getting Started
**Ansible Tower** knwon as Red Hat **Ansible Automation Platform** is a console interface for Ansible.

### Concepts
- **Project**: collections of ansible playbooks. they can reside localy on the tower server, or on vesion control supported by tower(eg. git).

- **Inventory**: An Inventory is a collection of hosts against which jobs may be launched, the same as an Ansible inventory file. 

- **Credentials**: used by tower to authenticate when launching jobs against machines, to import projects from version control servers,

- **Templates**: parametrable jobs.

- **Jobs**: A job is basically an instance of Tower launching an Ansible playbook against an inventory of hosts.

### Workshop Examples
See This [Tuto](https://redhatgov.io/workshops/ansible_automation)

### Inventories
1. Create a Group : web. In your playbook you put `hosts: web`
2. Create Hosts.
![to](/docs/images/ansible-tower-inventory-1.png)
![to](/docs/images/ansible-tower-inventory-2.png)


### Credentials
- CREDENTIAL TYPE: Click on the magnifying glass, pick Machine. 
- PRIVILEGE ESCALATION METHOD: sudo

Differents methods can be used:
- user/password:
- SSH Private Key. Use the **~/.ssh/id_rsa** of the tower machine. However, tower machine must be able to connect to remote machine without password, see **ssh-copy-id**.

![to](/docs/images/ansible-tower-credentials.png)
OR
![to](/docs/images/ansible-tower-credentials-sshkey.png)

### Create a Project
- SCM URL: https://github.com/ansible/workshop-examples.git
![to](/docs/images/ansible-tower-create-project.png)

List of Projects:
![to](/docs/images/ansible-tower-projects.png)


### Create a Job Template and Run a Job
- CREATE JOB TEMPLATE
  - Name: Install Apache
  - INVENTORY: vms-dev
  - CREDENTIALS: dev-creds
  - PROJECT: Ansible Workshop Examples
  - PLAYBOOK: apache_install.yml
![to](/docs/images/ansible-tower-create-template.png)

List of templates:
![to](/docs/images/ansible-tower-templates.png)

### Workflow Template
![to](/docs/images/ansible-tower-workflow-template.png)

### Variables
![to](/docs/images/ansible-tower-variables.png)

### Add Approval to workflow 
Add Approval to Workflow. outgoing Link  must be "on success" run type. 
![to](/docs/images/ansible-tower-approval.png)

When you run your worflow, you will have a notification to approve or deny:
![to](/docs/images/ansible-tower-approval-notification.png)

### Trial Download
<a>http://www.ansible.com/tower-trial</a>

### Installation
Steps (tested on a Rhel7):
- Download tower and untar it
  ~~~sh
  curl --insecure -o "/opt/ansible-tower-setup-latest.tar.gz" "https://releases.ansible.com/ansible-tower/setup/ansible-tower-setup-latest.tar.gz"
  ~~~

- Edit the **inventory** file, and define passwords.

- Run the Installation on the Tower
  ~~~sh
  cd /opt/ansible-tower-setup-3.8.6-2/
   . ./setup.sh
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

Console: https://TOWER_SERVER_NAME/
- admin/changeit

### Config Files 
- /etc/tower/conf.d/

### Error logs
- **/var/log/tower**
- Nginx logs are http logs
- can be configured in /etc/tower/conf.d/ 

### Unable to login to Tower via HTTP
Error : ERR_SSL_KEY_USAGE_INCOMPATIBLE

See: https://access.redhat.com/solutions/6955072

See: https://docs.ansible.com/ansible-tower/latest/html/administration/troubleshooting.html#error-logs

### Reset Admin Password
~~~sh
# awx-manage changepassword admin
~~~

### Role-Based Access Controls - RBAC
- A **role** is essentially a collection of capabilities.
- **User Type**: There are three user types
  - **Normal User**: read and write access limeted to inventory and projects for which he was has been granted.
  - **System Auditor**: auditors have read-only access to all obejects.
  - **System Administrator**: administrators have admi/read/write to all objects.

- **Teams**: provide a means to implement role-based access control schemes and delegate responsibilities across organizations.   

Create a Team: **Prod_Exploit**

![a](/docs/images/ansible-tower-team-users.png)

Give Prod_Exploit Team access on Inventory: All Users of that team will have that access.

![a](/docs/images/ansible-tower-rbac-inventory-access.png)


### Best Practices
- **Inventories**:  Inventories should be logically divided based on the environment, like development, testing, and production.
-  

### Docs
- Excellent Ansible Workshops: https://redhatgov.io/workshops/ansible_automation
- https://goetzrieger.github.io/ansible-tower-getting-started
- https://www.freekb.net/Articles?tag=Ansible
- https://docs.ansible.com/ansible-tower/