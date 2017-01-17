#!/bin/bash

# Print out container IP address
echo "This container IP address is: `hostname -i`"

# Set-up the path to where the node.js modules were installed
export NODE_PATH=/opt/SmartHome-Demo/node_modules/

# Start all different OCF servers available
for file in `ls -1 /opt/SmartHome-Demo/ocf-servers/js-servers/*.js`
do
	/usr/bin/node $file -s &
	sleep 0.2
done

# Start the Home Gateway
/usr/bin/node /opt/SmartHome-Demo/gateway/gateway-server.js -r &
sleep 0.2

# Start IoT REST API server
/usr/bin/node /opt/SmartHome-Demo/node_modules/iot-rest-api-server/index.js &

keepgoing=true

trap "keepgoing=false" SIGINT

echo "Press [CTRL+C] to stop.."

while $keepgoing
do
	:
done
