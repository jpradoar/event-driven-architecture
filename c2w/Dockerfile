FROM ubuntu:22.04

RUN apt-get update && \
apt-get update && apt-get install -y curl wget ansible unzip bash git openssh-client jq && \
wget -q https://releases.hashicorp.com/terraform/1.9.5/terraform_1.9.5_linux_386.zip && \
unzip terraform_1.9.5_linux_386.zip && \
mv terraform /usr/local/bin/terraform && \
chmod +x /usr/local/bin/terraform && \
rm LICENSE.txt terraform_1.9.5_linux_386.zip

ENTRYPOINT ["/bin/bash"]


