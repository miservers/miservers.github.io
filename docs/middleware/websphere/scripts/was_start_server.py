#
# Start a WAS Server
#  $WAS_INSTALL_ROOT/profiles/Dmgr01/bin/wsadmin.sh -lang jython -conntype SOAP -host rhel2 \
#                                                 -username wasadmin -password changeit \
#		            							 -f was_create_server.py serverName nodeName cellName
#
#
import sys

serverName = sys.argv[0]
nodeName = sys.argv[1]
cellName = sys.argv[1]


server = AdminControl.completeObjectName('cell=%s,node=%s,name=%s,type=Server,*'%(cellName, nodeName, serverName))
print server

serverState = AdminControl.getAttribute(server, 'state')

if serverState != 'STARTED':
  AdminControl.startServer(serverName, nodeName)
else:
  print 'Server already stareted'

