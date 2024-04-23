---
layout: default
title: Ansible
parent:  Ansible
grand_parent: DevOps
nav_order: 1
---


### Concepts
Playbook: means ansible configuration files. It contains a list of tasks that will be executed on set of specified hosts.

### Inventory (Hosts)
Ansible use inventory file to keep track of the hosts belonging to your infrastructure. Default inventory location is **/etc/ansible/hosts**, but you can any other file and use **-i** option. 

Exemple of an **inventory** file:
~~~
[appservers]
alma1
alma2
10.2.0.4
~~~

To list an inventory hosts:
~~~sh
ansible-inventory -i inventory --list
~~~

Ping All inventory hosts:
~~~sh
ansible all -i inventory -m ping
~~~

### Execute ad-hoc commands
Syntex: 
~~~sh
ansible [pattern] -m [MODULE] -a {COMMAND OPTIONS}
~~~

Examples:
~~~sh
 ansible  appservers -i inventory -m ping
~~~

### Connection Methods
By default Ansible assumes you are using SSH keys to connect to remote machines. That is recommended but you can use user/password method.

- SSH Keys Method: 
  ~~~sh
   ssh-copy-id username@remote_server
  ~~~

- User/Password Method: 

  ~~~sh
   ansible appservers -i inventory -m ping -u REMOTE_USER --ask-pass
  ~~~


### Variables
~~~
vars:
  http_port: 8080
  install_dir: /opt/tomcat
~~~

{% raw %}
variables can be refered by "{{var name}}"
{% endraw %}

[How to pass extra variables to an Ansible playbook](https://www.redhat.com/sysadmin/extra-variables-ansible-playbook)

### Modules
- **shell**: run shell commands.
- **group**: create a unix group.
- **user**: creates unix users.
- **file**: create files/directories.
- **copy**: copies files.
- **unarchive**: unpack an archive. It can copy the archive from the control machine or download it. 
- **blockinfile**: Insert/update/remove a text block in a file
- **setup**: to get remote host configuration(ansible_facts)
- **systemd_service**: Alias **systemd**, Controls systemd units (services, timers, and so on) on remote hosts.


### Privilege escalation: become
Execute tasks with root privileges.


### Execute a Playbook
~~~sh
ansible-playbook -i prod-inventory tomcat-playbook.yml 
~~~

### Create a Symbolic Link
~~~yml
---
- hosts: testserver
  tasks:
    - name: Create a symlink to the JDK
      file:
        src: /opt/jdk-22
        dest: /opt/jdk
        state: link
~~~

### Create a User
~~~yml
- name: Create webadmin user
      user:
        name: webadmin
        password: $5$YQXOijrsiwvkIEMJ$SmB42.jlkrOyg0G/QArrHxV6rqzL3p2
        group: web
        state: present
~~~

Password id Genretated with:
~~~sh
mkpasswd --method=sha-256 changeit
~~~

### Insert at the end of File
~~~yml
  tasks:
    - name: Setup the  PATH
      blockinfile:
        path: /home/webadmin/.bash_profile
        insertafter: 'EOF'
        block: |
          export JAVA_HOME=/opt/jdk
          export PATH=$JAVA_HOME/bin:$PATH
~~~

### Debug
Display a message with **when** condition
~~~yaml
- name: show a message when the file exist
      debug:
        msg: /tmp/{{ file_name }} already exists
      when: myfile_exists is succeeded
~~~

Display a Variable Value after a **register** for example:
~~~yaml
- debug:
        var: myfile_exists
~~~

### Tests

Jinja2 tests allow us to evaluate conditionals using the **is** keyword.



### Templates
Template are proccessed by [Jinja2 template language](http://jinja.pocoo.org/docs/)

Example of template personalising tomcat http port:
- Define vars:
~~~yaml
vars:
    tomcat_http_port: 8180
    catalina_home: /opt/tomcat
~~~

- Copy server.xml into  templates/server.xml.j2 and edit it:
{% raw %}
  ~~~xml
  <Connector port="{{ tomcat_http_port }}" protocol="HTTP/1.1"
               connectionTimeout="20000"
  ~~~
{% endraw %}

- Create task
{% raw %}  
  ~~~yaml
  - name: Apply server.xml Template
       template:
         src: templates/server.xml.j2
         dest: "{{catalina_home}}/conf/server.xml"
  ~~~
{% endraw %}

- Apply the playbook
~~~sh
ansible-playbook -i ../prod-inventory playbook.yml
~~~

### Ansible Facts
Facts are remote hosts configuration, including OS, IP, FS, etc. You can access this data throughout **ansible_facts** variable, or via **setup** module.

- Using **ansible_facts** variable: add this task to your playbook

  ~~~yaml
  - name: Print all available facts
    ansible.builtin.debug:
      var: ansible_facts
  ~~~

- Using **setup** module:

  ~~~sh
  ansible web -i inventory -m setup
  ~~~

For example, to reference remote host OS type and release :

{% raw %}  
  ~~~jinja2
  {{ ansible_facts['ansible_distribution'] }}
  {{ ansible_facts['ansible_distribution_major_version'] }}
~~~
{% endraw %}  

### Loops, Handlers
- **Loop**:  `with_items`.
- **Handler**: using `notify` keyword, operations you want to run when a change is made on a machine. 

Example: playbook.yaml
~~~yaml
---
- hosts: web
  become: yes
  vars:
    httpd_packages:
      - httpd
      - mod_ssl

  tasks:
    - name: install httpd packages
      package:
        name: "{{ item }}"
        state: present
      with_items: "{{ httpd_packages }}"
      notify: Restart apache

  handlers:
    - name: Restart apache
      ansible.builtin.systemd:
        name: httpd
        state: restarted
~~~

**Loop Until**
~~~yaml
---
- name: localhost play
  hosts: localhost
  tasks:
  - name: Test Until
    shell: ps -ef | grep -v grep | grep 'Hello'
    register: result
    retries: 5
    delay: 1
    until: result.stdout is search 'Hello'
~~~



### Systemd: restart a service
Start Apache using systemd module. 
~~~yaml
---
- hosts: web
  tasks:
  - name: reload systemd daemons
    systemd:
      daemon_reload: yes

  - name: gather service facts
    ansible.builtin.service_facts:

  - name: start apache
    become: yes
    become_user: root
    systemd:
      name: httpd
      state: 'started'
      enabled: yes
    when: ansible_facts.services['httpd.service'] is defined and ansible_facts.services['httpd.service'].state != 'running'
~~~

### Vault
Ansible Vault is used to encrypt playbooks using password. 

Encrypt a Playbook:
~~~sh
ansible-vault encrypt  playbook.yml
~~~

To view the decrypted content:
~~~sh
ansible-vault view playbook.yml
~~~

When you want to execute the playbook, you will prompted to enter the password
~~~sh
ansible-playbook -i inventory playbook.yml --ask-vault-pass

Vault password: 
~~~

To avoid being prompted for password, you can use Vault password file:
  
  - Create pasword file

  ~~~sh
  echo "changeit" > .vault_password.txt

  chmod 0600 .vault_password.txt
  ~~~

  - Use the it

  ~~~sh
  ansible-playbook -i inventory playbook.yml --vault-password-file path/to/.vault_password.txt
  ~~~

To avoid vault password option in command line, you can use `export ANSIBLE_VAULT_PASSWORD_FILE=path/to/.vault_password.txt`, or add the vault password to `ansible.cfg` 

### Documentation
- [freekb](https://www.freekb.net/Articles?tag=Ansible)
- [playbooks best practices](https://docs.ansible.com/ansible/2.8/user_guide/playbooks_best_practices.html)
- [Templates For Tomcat](https://github.com/mitre/ansible-cis-tomcat-hardening)

