#
# Deploy an Application on WAS
#

# Debug
# print AdminApp.options()

ear_url='/opt/IBM/WebSphere/AppServer/installableApps/DefaultApplication.ear'
nodeName='rhel3CellNode01'
cellName='Cell01'
serverName='server1'

options='[-node '+ nodeName + ' -cell ' + cellName + ' -server ' +  serverName + ']' 
AdminApp.install(ear_url , options)

AdminConfig.save()
