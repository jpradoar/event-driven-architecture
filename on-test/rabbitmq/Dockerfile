FROM bitnami/rabbitmq:3.11.17-debian-11-r2
USER root
RUN mkdir -p /opt/bitnami/rabbitmq/.rabbitmq/ && \
	chmod 600 /opt/bitnami/rabbitmq/.rabbitmq/* && \
	rabbitmq-plugins enable rabbitmq_management rabbitmq_management_agent rabbitmq_web_stomp rabbitmq_web_stomp_examples rabbitmq_mqtt rabbitmq_prometheus rabbitmq_top rabbitmq_web_dispatch rabbitmq_web_mqtt rabbitmq_event_exchange rabbitmq_amqp1_0 rabbitmq_peer_discovery_k8s rabbitmq_tracing rabbitmq_stomp rabbitmq_peer_discovery_aws rabbitmq_federation rabbitmq_federation_management
