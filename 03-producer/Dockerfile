FROM alpine:latest
WORKDIR /app
ADD ./templates /app/templates/
ADD ./api.py /app/api.py
RUN apk add python3 py3-pip bind-tools && pip3 install flask pika prometheus_client 

CMD [ "python3", "-u", "./api.py" ] 