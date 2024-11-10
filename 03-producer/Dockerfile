FROM alpine:3.19.0
WORKDIR /app
COPY ./templates /app/templates/
COPY ./api.py /app/api.py
RUN adduser -D userx \
	&& apk add --no-cache python3 py3-pip bind-tools \
	&& python3 -m venv /venv \
	&& /venv/bin/pip install --no-cache-dir flask pika prometheus_client
USER userx
CMD ["/venv/bin/python3", "-u", "./api.py"]