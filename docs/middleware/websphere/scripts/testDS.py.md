---
layout: default
title: Websphere - Jython - testDS 
parent:  Websphere - Jython
---

~~~py

# Test All Data Sources Connections
#
# testDS.py                           
# <profile_home>/bin/wsadmin.sh -f             
#                  /path/to/testDS.py 

datasources = AdminConfig.list('DataSource').splitlines()

for datasource in datasources:
	name = AdminConfig.showAttribute(datasource, 'name')
	
	if ( name != "DefaultEJBTimerDataSource" ):
		try:
			AdminControl.testConnection(datasource)
			print "Testing " + name + " successful "
		except:
			print "Testing " + name + " failed " 


~~~