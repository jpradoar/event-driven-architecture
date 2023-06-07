FROM alpine:3.17.0
WORKDIR /app
ADD ./db.py /app/db.py
RUN apk update; apk add curl wget unzip python3 py3-pip && pip3 install flask pika prometheus_client mysql-connector
CMD [ "python3", "-u", "./db.py" ]

