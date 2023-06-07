#!/usr/bin/python3
#
##############################################################
################# LIBRERIAS PARA LA APP ######################
import pika                                     # Para trabajar con RabbitMQ.
import os                                       # Para obtener las variables de entorno.
import json                                     # Para trabajar con JSON.
import sys                                      # No me acuerdo.
import time                                     # Para manejar datetime y similar.
import logging                                  # Para login a consola (stdout).
from prometheus_client import start_http_server # Para levantar el http_server.
from prometheus_client import Info, Counter     # Para exponer metricas de info y contadores.
#
##############################################################


##############################################################
#### CONFIGURACIONES GENERICAS Y DECLARACION DE VARIABLES ####
#
#
# Con esto le doy formato a los logs que voy a exponer. 
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
#
#
# Genero el info para las metricas que voy a exponer para prometheus.
metric_info     = Info('pubsub_version', 'build version of pubsub')
# Declaro el puerto que voy a usar para que prometheus haga el scraping de metricas.
metrics_port    = 9090
#
# Como no quiero que mi codigo tenga hardcodeados valores utilizo el environ.get 
# para consumir las variables de entorno del POD.  
# Y asi también puedo reutilizar este codigo.
mqtthost            = os.environ.get('mqtthost')    #"rabbitmq"
mqttvhost           = os.environ.get('mqttvhost')   #"/"
mqttuser            = os.environ.get('mqttuser')    #"admin"
mqttpass            = os.environ.get('mqttpass')    #"admin"
mqttport            = os.environ.get('mqttport')    #5672
queue               = os.environ.get('ori_queue')   #"infra"
destination_queue   = os.environ.get('dest_queue')  # other
connection_attempts = 5
retry_delay         = 5
#
#
# Parametros de conexión para el rabbitMQ 
credentials = pika.PlainCredentials(mqttuser, mqttpass)
parameters  = pika.ConnectionParameters(host=mqtthost,port=mqttport,virtual_host=mqttvhost,credentials=credentials,connection_attempts=connection_attempts, retry_delay=retry_delay )
connection  = pika.BlockingConnection(parameters)
channel     = connection.channel()
# Por si no existe la queue, la creo. 
channel.queue_declare(queue=queue, durable=True)


################################################################
########################### GENERICO ###########################
#
# Genero una funcion para el envio de metricas informativas en prometheus
# Esto tambien podria aplicar a un tipo de metrica tipo Counter, para contabilizar la cantidad de llamadas a una funcion en la api o similar.
def metrics_info():
  metric_info.info({'name':'pubsub', 'version': '1.0.0', 'owner': 'jpradoar'})
#
# Genero una función para reciclar el envío de mensajes, notificaciones y/o logs.
def sendmsg(message):
  logging.info(message)
#
################################################################


################################################################
###################### CONSUMIR MENSAJES #######################
#
# Este callback es llamado por la libreria Pika. Inediatamente despues que recibo un mensaje, 
# lo transformo en UTF-8 y lo envío a la funcion de parseo .
def callback(ch, method, properties, body):
  parseMsg(body.decode("utf-8"))
#
#
# Al recibir la variable "data" esta contiene el Json que recibo del callback. 
# En este punto separo las variables obtenidas en el json para reutilizarlas.
def parseMsg(data):
  data        = json.loads(data)
  client      = data['client']
  namespace   = data['namespace']
  product     = data['product']
  environment = data['environment']
  archtype    = data['archtype']
  hardware    = data['hardware']
  trace_id    = data['MessageAttributes']['trace_id']
  sendmsg("  *[GenericPubSub] Message: " + str(data) + "\n")
  sendmsg("  *[GenericPubSub] Message trace_id: " + str(trace_id) + "\n")
  # En este punto llamo a la funcion PubMessage y le paso las variables seleccionadas.
  PubMessage(client,product) 
# 
#
# Esta funcion es la que se encarga de enviar el mensaje a la cola de destino declarada en las variables generales.
# Recibe los parametros filtrados del JSON original y genero un nuevo JSON 
# con solo la información que necesito enviar a la nueva cola.
def PubMessage(client,product):    
  #channel.queue_declare(queue=destination_queue, durable=True) 
  message = "  *[GenericPubSub] Send messaje to queue: ["+ destination_queue +"]"
  sendmsg(message)
  data = '{"client": "'+client+'","nueva_clave": "nuevo_valor","product": "'+product+'"}'
  channel.basic_publish(exchange='', routing_key=destination_queue, body=data)
  sendmsg("  *[GenericPubSub] " + data)    
#
#
# Genero una funcion main para colocar todo lo que necesito ejecutar.
# Envio un mensaje de que se conecto a la queue y que espera por nuevos mensajes.
# También levanto un http_server para prometheus y exponer las metricas de la app
# Imprimo las metricas informativas para prometheus y finalmente me pongo a consumir mensajes.
def main():
  sendmsg("  *[GenericPubSub] Queue [" + queue + "] ")
  channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
  sendmsg("  *[GenericPubSub] Waiting messages in Queue: [ "+ queue +" ] ")
  start_http_server(metrics_port)
  metrics_info()
  channel.start_consuming()
#
############################################################


# Por comodidad esto lo dejo siempre igual asi lo uso como template.
if __name__ == '__main__':
  main()