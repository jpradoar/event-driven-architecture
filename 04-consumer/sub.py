#!/usr/bin/python3
import pika, os
import json
import sys
import subprocess
import time      
import logging   # Para login a consola (stdout)
from prometheus_client import start_http_server # usado para levantar el http_server
from prometheus_client import Info, Counter     # usado para exponer metricas de info y contadores

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

metric_info     = Info('consumer_version', 'build version of consumer')
metrics_port    = 9090

mqtthost    = os.environ.get('mqtthost')  #"rabbitmq"
mqttvhost   = os.environ.get('mqttvhost')  #"/"
mqttuser    = os.environ.get('mqttuser')  #"admin"
mqttpass    = os.environ.get('mqttpass')  #"admin"
mqttport    = 5672
queue       = os.environ.get('queue')  #"infra"


# Abro una conexión con el rabbit para enviar y recibir los mensajes. 
credentials = pika.PlainCredentials(mqttuser, mqttpass)
parameters  = pika.ConnectionParameters(host=mqtthost,port=mqttport,virtual_host=mqttvhost,credentials=credentials,connection_attempts=5, retry_delay=5 )
connection  = pika.BlockingConnection(parameters)
channel     = connection.channel()
channel.queue_declare(queue=queue, durable=True)

# Genero una funcion para el envio de metricas informativas en prometheus
# Esto tambien podria aplicar a un tipo de metrica Counter para contabilizar la cantidad de llamadas a una funcion en la api.
def metrics_info():
  metric_info.info({'name':'consumer', 'version': '1.0.0', 'owner': 'jpradoar'})

# Genero una función para reciclar el envío de mensajes, notificaciones y/o logs.
def sendmsg(message):
  logging.info(message)

# Esta funcion es la que se encarga de enviar el mensaje a la cola para que el DBWriter agregue el cliente a la DB de clientes.
# recibe los parametros filtrados del JSON original que envio la api customer-portal y genera un nuevo JSON que lo envia a la cola de clientes
# donde será utilizado para escribir dicha data en la DB
def WriteDB(client,archtype,hardware,product):     
  message = "  *[Consumer] Send messaje to dbwriter to create new user in DBCLIENTS: [" + client + "] "
  sendmsg(message)
  #channel.queue_declare(queue='clients', durable=True)
  data = '{"client": "'+client+'","archtype": "'+archtype+'","hardware": "'+hardware+'","product": "'+product+'"}'
  channel.basic_publish(exchange='', routing_key='clients', body=data)
  sendmsg("  *[Consumer] " + data)    

# Esta funcion recibe el environment donde se va a deployar, el namespace y el nombre del cliente
# Con todo eso genera un namespace y deploya el cliente.
# En este caso para ahorrar APIs uso un subprocess para ejecutar un comando de linux  (helm).
# Idealmente deberia ser otra api o proceso que ejecute esto pero a fines de la demo funciona bien como ejemplo. 
def executeDeployment(environment,client,product):
  #
  # Esta parte se ve fea, pero es solo para la demo. 
  # 
  subprocess.run("helm repo add bitnami https://charts.bitnami.com/bitnami", shell=True)
  sendmsg("  *[Consumer] [run]  helm upgrade -i -n "+client+" --create-namespace "+client+"  bitnami/"+product+" ")
  subprocess.run("helm upgrade -i -n mqtt-poc --create-namespace "+client+" bitnami/"+product+" ", shell=True)
  time.sleep(3)  # Los sleep solo los uso para que en la demo se vea con un poco de delay
  sendmsg("  *[Consumer] [DEPLOYMENT] client: [" + client + "] DONE" )

# Envio un mensaje a la cola de Status para declarar que el proceso termino.
# Esta cola la podria usar para mostrarle al cliente el estado de su deployment en tiempo real. 
def finish_message(client):
  channel.queue_declare(queue='event-status', durable=True)
  data = '{"client": "'+client+'","Status": "Finished"}'
  channel.basic_publish(exchange='', routing_key='event-status', body=data)
  message = "  *[Consumer] [DONE] Message event-status: [" + data + "] sent to queue: [event-status]"
  sendmsg(message)

# El mensaje que debe recibir es un json similar a esto:  {"client":"ClientX", "namespace": "ClientX", "environment": "development"}
def parseMsg(data):
  data        = json.loads(data)
  client      = data['client']
  namespace   = data['namespace']
  product     = data['product']
  environment     = data['environment']
  archtype    = data['archtype']
  hardware    = data['hardware']
  trace_id    = data['MessageAttributes']['trace_id']
  sendmsg("  *[Consumer] Message: " + str(data) + "\n")
  sendmsg("  *[Consumer] Message trace_id: " + str(trace_id) + "\n")
  time.sleep (1)
  WriteDB(client,archtype,hardware,product)
  time.sleep (1)
  executeDeployment(environment, client, product)
  time.sleep (1) 
  finish_message(client)
 
def callback(ch, method, properties, body):
  parseMsg(body.decode("utf-8"))


def main():
  sendmsg("  *[Consumer] Queue [" + queue + "] ")
  channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
  sendmsg("  *[Consumer] Waiting messages in Queue: [ "+ queue +" ] ")
  start_http_server(metrics_port)
  metrics_info()
  channel.start_consuming()

if __name__ == '__main__':
  main()
