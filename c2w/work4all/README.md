# Run All in docker container


### Build docker container
	docker build -t c2w .


### Run dokcer container
	docker run --rm -itd --name c2w \
	-p 10022:22 \
	-v /home/$(whoami)/.github:/root/.ssh  c2w


### Access as normal remote linux 
	ssh root@localhost -p 10022


### Delete container
    docker rm -f c2w
