FROM alpine:3.17.0
WORKDIR /app
ADD ./db.py /app/db.py
RUN adduser -D userx; apk update; apk add mysql-client python3 py3-pip && pip3 install pika prometheus_client mysql-connector 
USER userx
CMD [ "python3", "-u", "./db.py" ]

