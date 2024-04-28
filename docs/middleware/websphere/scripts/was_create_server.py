
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
