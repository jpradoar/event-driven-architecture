FROM alpine:3.20.3
RUN apk update \
&& apk add curl \
&& curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" \
&& chmod +x kubectl \
&& mv kubectl  /usr/local/bin/
ENTRYPOINT ["/bin/sh","-c","kubectl get events -Aw"]
