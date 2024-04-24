---
layout: default
title: Shell, Command, Script
parent:  Ansible
grand_parent: DevOps
nav_order: 3.2
---


### Shell 
Shell module is used to execute shell commands on remote servers. command are proccessed in shell environment: possibility of using shell-specific features(`<, >, >>, &, |`), and shell variables like `$HOSTNAME`

  - Example:

  ~~~yaml
  - name: Check if a process is running
    ansible.builtin.shell: ps aux | grep 'nginx' | grep -v grep
    register: process_status
    failed_when: process_status.rc != 0
  ~~~

### Command
idem to shell, command module runs commands on selected nodes. BUT the commands will not be run through the shell. So variables like `$HOSTNAME` and operations like `"*", "<", ">", "|", ";" and "&"` will NOT work!.
  
  - Example:

  ~~~yaml
  - name: Change to somedir/ and run the command  if /path/to/database does not exist.
    command: /usr/bin/make_database.sh db_user db_name
    become: yes
    become_user: db_owner
    args:
      chdir: somedir/
      creates: /path/to/database
  ~~~ 

### Script
script module runs a local script on a remote node after transferring it.
  
  - Example:

  ~~~yaml
  - name: Run a script only if file.txt does not exist on the remote node
    ansible.builtin.script: /some/local/create_file.sh --some-argument 1234
    args:
      creates: /the/created/file.txt
  ~~~