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
        [ -lang  language]  
        [ -profileName profile]  
        [ -conntype  
                SOAP
                        [-host host_name]
                        [-port port_number]
                        [-user userid]
                        [-password password] | 
        [ -f <script_file_name>] 
        [ script parameters ]
		...
~~~

Example :
~~~sh
$WAS_INSTALL_ROOT/profiles/Dmgr01/bin/wsadmin.sh -lang jython -conntype SOAP -host rhel2 \
                                                 -username wasadmin -password changeit \
		            							 -f was_create_server.py server_name node_name
~~~

### wsadmin Objects
There are 5 Objects:
1. Help
2. AdminConfig: used to create or change WAS configuration
3. AdminControl: deal with running objects in WAS
4. AdminApp: install, modify, administer applications
5. AdminTask:  used to run an administrative command

### Create a Server
was_create_server.jy 
~~~py
import sys

server_name = sys.argv[0]
node_name = sys.argv[1]

# Get Node ID, on which you are adding the new server
node = AdminConfig.getid('/Node:%s/' %node_name)

print node

# Create the server
attrs = [ ['name', server_name] ]
AdminConfig.create('Server', node, attrs)

# Save the Configuration
AdminConfig.save()
~~~

### Create a Data Source

### Deploy a an Application
