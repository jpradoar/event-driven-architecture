FROM debian:bookworm-slim

ARG DEBIAN_FRONTEND=noninteractive
ENV LANG=es_ES.UTF-8
ENV LANGUAGE=es_ES:es
ENV LC_ALL=es_ES.UTF-8
ENV PIP_BREAK_SYSTEM_PACKAGES=1

RUN apt-get update; apt-get install -y locales wget gpg curl unzip iputils-ping apt-utils openssh-server git ansible \
    && sed -i '/es_ES.UTF-8/s/^# //g' /etc/locale.gen \
    && locale-gen es_ES.UTF-8 \
    && update-locale LANG=es_ES.UTF-8 LC_ALL=es_ES.UTF-8 \
    && locale-gen \
    && mkdir -p /var/run/sshd \
    && echo 'root:debian12' | chpasswd \
    && sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config \
    && echo 'PermitUserEnvironment yes' >> /etc/ssh/sshd_config  \
    && sed -i 's/#PermitRootLogin yes/PermitRootLogin yes/g' /etc/ssh/sshd_config \
    && sed -i 's/# alias l/alias l/g'  /root/.bashrc \
    && echo "PS1='\\[\\e[1;91m\\]\\u@\\h\\[\\e[0m\\]:\\w\\$ '" >> /root/.bashrc \
    && echo '\n\n*** CONTAINER TO WORK (c2w) ***\n\n' > /etc/motd \
	&& wget -q https://releases.hashicorp.com/terraform/1.12.2/terraform_1.12.2_linux_amd64.zip \
	&& unzip terraform_1.12.2_linux_amd64.zip \
	&& mv terraform /usr/local/bin/terraform  \
	&& chmod +x /usr/local/bin/terraform \
    && curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install --bin-dir /usr/local/bin --install-dir /usr/local/aws-cli --update

EXPOSE 22 

CMD ["/usr/sbin/sshd", "-D"]
