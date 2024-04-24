---
layout: default
title: WSADMIN
parent: WebSphere
grand_parent: Middleware
nav_order: 3
---

### Getting Started
The wsadmin tool runs scripts. You can use the wsadmin tool to manage application servers as well as the configuration, application deployment, and server runtime operations.

~~~
$WAS_INSTALL_ROOT/profiles/profile_name/bin/wsadmin.sh
~~~


To connect, it uses:
- **$WAS_INSTALL_ROOT/profiles/profile_name/properties/wsadmin.properties**
~~~props
com.ibm.ws.scripting.connectionType=SOAP
com.ibm.ws.scripting.port=8879
com.ibm.ws.scripting.host=rhel2
com.ibm.ws.scripting.defaultLang=jython
~~~

- Or parameters with syntax:
~~~sh
./wsadmin.sh 
        [ -c <command> ] 
        [ -p <properties_file_name>] 
        [ -f <script_file_name>] 
        [ -lang  language]  
        [ -profileName profile]  
        [ -conntype  
                SOAP
                        [-host host_name]
                        [-port port_number]
                        [-user userid]
                        [-password password] | 
        [ script parameters ]
		...
~~~

Example :
~~~sh
$WAS_INSTALL_ROOT/profiles/Dmgr01/bin/wsadmin.sh -lang jython -conntype SOAP -host rhel2 \
                                         -username wasadmin -password changeit -f was_create_server.py 
~~~

### wsadmin Objects
There are 5 Objects:
1. Help
2. AdminConfig: used to create or change WAS configuration
3. AdminControl: deal with running objects in WAS
4. AdminApp: install, modify, administer applications
5. AdminTask:  used to run an administrative command

### Create a Server
was_create_server.py 
~~~py
# Get Node ID, on which you are adding the new server
node_name = 'rhel3CellNode01'
node = AdminConfig.getid('/Node:%s/' %node_name)

print node

# Create the server
server_name='server2'
attrs = [ ['name', server_name] ]
AdminConfig.create('Server', node, attrs)

# Save the Configuration
AdminConfig.save()
~~~

then run:
~~~sh
$WAS_INSTALL_ROOT/profiles/Dmgr01/bin/wsadmin.sh -lang jython -conntype SOAP -host rhel2 \
                                        -username wasadmin -password changeit \
										-f was_create_server.py server_name node_name
~~~

### Create a Data Source

### Deploy a an Application
