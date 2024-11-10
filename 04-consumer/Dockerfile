FROM alpine:3.17.0
WORKDIR /app
ADD ./sub.py /app/sub.py
RUN apk update; apk add curl wget unzip python3 py3-pip aws-cli && pip3 install flask pika pymsteams prometheus_client && \
wget -nv https://get.helm.sh/helm-v3.10.1-linux-amd64.tar.gz && \
tar -xzf helm-v3.10.1-linux-amd64.tar.gz && \
mv linux-amd64/helm /usr/local/bin/ && \
chmod +x /usr/local/bin/helm && \
rm -rf linux-amd64 helm-v3.10.1-linux-amd64.tar.gz 
CMD [ "python3", "-u", "./sub.py" ]

#&& \
#curl -LO https://dl.k8s.io/release/v1.26.0/bin/linux/amd64/kubectl && \
#mv kubectl /usr/local/bin/kubectl && \
#chmod +x /usr/local/bin/kubectl 