# Run All in docker container


### Build docker container
	docker build -t c2w .


### Create folder to share between container and your local
	mkdir -p /tmp/c2w


### Run dokcer container
	docker run \
	--rm \
	-itd \
	--name c2w \
	-v /tmp/c2w:/data \
	c2w:latest

### Work in container
	docker exec -it c2w:latest bash
