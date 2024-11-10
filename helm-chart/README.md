# How to run

### Deploy with custom namespace 
	helm upgrade -i --create-namespace -n default mqtt .

### Delete deploy and VPCs
	helm delete mqtt && kubectl delete pvc data-mqtt-rabbitmq-0
