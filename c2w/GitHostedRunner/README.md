# Github self-hosted runner in docker container 


### Build 
	docker build -t eda-hosted-runner .


### Run hosted runner
	docker run \
	--rm \
	-itd \
	--name eda-hosted-runner \
	--hostname eda-hosted-runner \
	-e RUNNER_TOKEN=YOUR_GITHUB_RUNNER_TOKEN_HERE \
	-e GITHUB_REPOSITORY_URL=https://github.com/jpradoar/event-driven-architecture \
	eda-hosted-runner:latest


### Using docker-compsoe 
	docker-compose up -d 