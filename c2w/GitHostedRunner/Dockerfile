FROM ubuntu:22.04

WORKDIR /actions-runner


ENV RUNNER_NAME="eda-hosted-runner"
ENV RUNNER_WORK_DIRECTORY="_work"
ENV GITHUB_REPOSITORY_URL="https://github.com/jpradoar/event-driven-architecture"
ENV RUNNER_TOKEN=""

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
apt-get install -y curl jq sudo tar git && \
rm -rf /var/lib/apt/lists/* && \
curl -o actions-runner-linux-x64-2.320.0.tar.gz -L https://github.com/actions/runner/releases/download/v2.320.0/actions-runner-linux-x64-2.320.0.tar.gz && \
tar xzf ./actions-runner-linux-x64-2.320.0.tar.gz  && \
rm -rf actions-runner-linux-x64-2.320.0.tar.gz && \
apt-get clean && \
useradd -m github-runner && \
mkdir -p /actions-runner && \
chown -R github-runner:github-runner /actions-runner  && \
echo "github-runner ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER github-runner

RUN sudo ./bin/installdependencies.sh && chmod +x ./config.sh ./run.sh

CMD ./config.sh --url $GITHUB_REPOSITORY_URL --token $RUNNER_TOKEN --name $RUNNER_NAME --work $RUNNER_WORK_DIRECTORY --unattended --replace && ./run.sh