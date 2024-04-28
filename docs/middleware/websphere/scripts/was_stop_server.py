#
# Start a WAS Server
#

cellName='Cell01'
nodeName='rhel3CellNode01'
serverName='server1'


server = AdminControl.completeObjectName('cell=%s,node=%s,name=%s,type=Server,*'%(cellName, nodeName, serverName))
print server

serverState = AdminControl.getAttribute(server, 'state')

if serverState == 'STARTED':
  AdminControl.stopServer(serverName, nodeName)
else:
  print 'Server already stopped'

