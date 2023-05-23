#!/usr/bin/python3
import os                                       # Para obtener las variables del Deployment
import pika                                     # Para rabbitmq
import json                                     # Para manejar los JSON
import mysql.connector                          # Para conectar al MariaDB
import datetime, time                           # Para manejo de tiempo
import logging                                  # Para manejo de log y STDOUT
from prometheus_client import start_http_server # Para levantar el http_server
from prometheus_client import Info              # Para exponer metricas

# Formateo el log FECHA - MENSAJE
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

# PROMETHEUS
metric_info     = Info('dbwriter_version', 'build version of dbwriter')
metrics_port    = 9090

# RABBIT
mqtthost    = os.environ.get('mqtthost') #"rabbitmq" 
mqttvhost   = os.environ.get('mqttvhost') #"/"
mqttuser    = os.environ.get('mqttuser') #"admin"
mqttpass    = os.environ.get('mqttpass') #"admin"
mqttport    = os.environ.get('mqttport') #
queue       = os.environ.get('queue') #"clients"
credentials = pika.PlainCredentials(mqttuser, mqttpass)
parameters  = pika.ConnectionParameters(host=mqtthost,port=mqttport,virtual_host=mqttvhost,credentials=credentials,connection_attempts=5, retry_delay=5)

# DATABASE
mysql_host  = os.environ.get('mysql_host') #"mariadb"  
mysql_user  = os.environ.get('mysql_user') #"admin"
mysql_pass  = os.environ.get('mysql_pass') #"admin"
mysql_db    = os.environ.get('mysql_db')   #"clients"

# TIEMPO
now         = datetime.datetime.now()
dateformat  = now.strftime("%Y-%m-%d")

# Genero una función para reciclar el envío de mensajes, notificaciones y/o logs.
def sendmsg(message):
  logging.info(message)

# Genero una metrica informativa para saber la version e info general
def metrics_info():
  metric_info.info({'name':'dbwriter', 'version': '1.0.0', 'owner': 'jpradoar'})

# Funcion que genera una conexión a una DB e inserta los datos recibidos en la misma. 
def WriteDB(sql,val):
  connector   = mysql.connector.connect(host=mysql_host,user=mysql_user,password=mysql_pass,database=mysql_db)
  db          = connector.cursor()
  db.execute(sql,val)
  connector.commit()
  sendmsg("  *[DBWriter] One record was inserted, RecordID:"+ str(db.lastrowid))
  db.close()
  connector.close()
  sendmsg("  *[DBWriter] Waiting messages in Queue: [ "+ queue +" ] ")  

# Función principal encargada de conectarse al MQTT Server, esperar mensajes y actuar en base al mensaje recibido.
def main():
  #validateMQTTConnection()
  connection  = pika.BlockingConnection(parameters)
  channel     = connection.channel()
  channel.queue_declare(queue=queue, durable=True) # Declaro y creo la queue si no existe

  def callback(ch, method, properties, body):
      parseMsg(body.decode("utf-8"))

  sendmsg("  *[DBWriter] Started and connected to Queue: [ "+ queue +" ] ")
  channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
  start_http_server(metrics_port)
  metrics_info()
  channel.start_consuming()


# Funcion para parsear los datos que recibo en formato json y generar una query de SQL
# El mensaje que debe recibe es un json similar a esto:  
# {"client":"ClientX", "archtype": "true", "hardware":"shared"}
def parseMsg(data):
  data        = json.loads(data)
  client      = data['client']
  archtype    = data['archtype']
  hardware    = data['hardware']
  product     = data['product']
  xdate       = dateformat
  license     = 'OpenSource'
  val         = (client,archtype,hardware,product,xdate,license)
  sql         = "INSERT INTO clients (client,archtype,hardware,product,xdate,license) VALUES (%s,%s,%s,%s,%s,%s)"
  WriteDB(sql,val)

# En general cuando uso docker-compose o kubernetes suele pasar que este servicio levanta antes que Rabbit.
# Por tal motivo valido si el Rabbit esta listo, sino espero 5 segundos. 
def validateMQTTConnection():
  while True:
      try:
          connection = pika.BlockingConnection(parameters)
          channel = connection.channel()
          break
      except pika.exceptions.AMQPConnectionError:
          sendmsg("  *[DBWriter] No se puede conectar a RabbitMQ, esperando 5 segundos para reconectar...")
          time.sleep(5)      

if __name__ == '__main__':    
  main()