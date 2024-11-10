#!/usr/bin/python3
from flask import Flask, jsonify, request, Response, render_template # para crear la api
from functools import wraps                     # no me acuerdo
import http.client                              # para levantar un http client
import json                                     # Para manejar los json
import pika                                     # para RabbitMQ
#import ssl                                      # Opcional solo para los casos que la conexión requiera ssl  (EJ RabbitMQ de AWS )
import datetime, time                           # manejo del tiempo
import os
import uuid                                     # para generar un hash unico que luego sera usado en los mensajes de MQTT
import socket                                   # para obtener el hostname del contenedor
from socket import gaierror
import logging                                  # para recopilar metricas de monitoreo y logs
from prometheus_client import start_http_server # para levantar el http_server
from prometheus_client import Info              # para prometheus
from threading import Thread                    # para ejecutan algunas cunciones en hilos separados


# Variables globales
mqtthost            = os.environ.get('mqtthost')  #"rabbitmq"
mqttvhost           = os.environ.get('mqttvhost') #"/"
mqttuser            = os.environ.get('mqttuser')  #"admin"
mqttpass            = os.environ.get('mqttpass')  #"admin"
queue               = os.environ.get('queue')     #"infra"
mqttport            = 5672
now                 = datetime.datetime.now()
dateformat          = now.strftime("%Y-%m-%d")      
myname              = socket.gethostname()
hostname            = str(myname+"@"+socket.gethostbyname(myname))
destination_queue   = os.environ.get('destination_queue') # "infra"
destination_RK      = os.environ.get('destination_RK') #"infra"
credentials         = pika.PlainCredentials(mqttuser, mqttpass)


# Log formato FECHA - MENSAJE
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

# Genero una función para reciclar el envío de mensajes, notificaciones, etc.
def sendmsg(message):
  logging.info(message)

# Genero un uudi para usarlo en trazas y mensajes de rabbitmq
def generate_trace_id():
  return str(uuid.uuid4())

# Genero una app en flask utilizando unos templates de html que estan alojados en templates/*
app = Flask(__name__, static_folder="templates")

# Validacion y autenticacion
# PENDIENTE DE VALIDAR CONTRA KEYCLOAK
def check_auth(username, password):
  return username == "admin" and password == "admin"

def not_authenticate():
  logging.error("-   *[Producer] Login Failed")
  return Response('Login fail: User and/or Password are wrong!\n', 401,  {'WWW-Authenticate': 'Basic realm="Login Required"'})

# Util si quiero que tenga que validar para acceder a algun recurso (como por ejemplo el formulario)
def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
      auth = request.authorization
      if not auth or not check_auth(auth.username, auth.password):
          return not_authenticate()
      return f(*args, **kwargs)
  return decorated


# Ruta para servir el favicon.ico y no muestre el error de 404 en los logs
@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

# Si es un GET esta accediendo al formulario para crear un nuevo recurso
# Si es un POST capturo la data del formulario y genero un json para enviarlo a una cola de RabbitMQ
@app.route('/', methods=['GET','POST'])
def my_form():
  if request.method == 'GET':
      return render_template('index.html')
  else:
      client      = request.form['client']
      namespace   = client+"-ns"   #request.form['namespace']
      environment = request.form['environment']
      archtype    = request.form['archtype']
      hardware    = request.form['hardware']
      product     = request.form['product']
      data = '{\
        "client":"'+client+'", \
        "namespace":"'+namespace+'", \
        "environment":"'+environment+'", \
        "archtype":"'+archtype+'", \
        "hardware":"'+hardware+'", \
        "product":"'+product+'", \
        "MessageAttributes": { \
            "event_type": { \
                "Type": "String", \
                "Value": "mycompany.'+myname+'.event.'+client+'.published" \
            }, \
          "published_on": "'+dateformat+'", \
          "trace_id": "'+generate_trace_id()+'", \
          "retrace_intent": "0" \
        }, \
        "Metadata": { \
          "host": "'+hostname+'", \
          "origing": "Cloud",      \
          "publisher": "'+myname+'" \
        } \
      }'   
      send_mqtt_msg(destination_queue, destination_RK, data)  
      sendmsg("-   *[Producer] " + data)  
      msginfo='{"client":"'+client+'","status":"Provisioning","product":"'+product+'"}'
      send_mqtt_msg("event-status", "event-status", msginfo)

      # El return lo genero para que devuelva el json que envia y luego de 3 segundos vuelva al index original.
      # para fines de la demo quiero que se vea que se genera el json que se envia al MQTT y que el 
      # trace_id se mantiene durante todo el proceso de deployment. 
      # Esto resulta muy útil cuando tengo que trackear un mensaje o troubleshootear un workflow completo. !!!!!
      return "<b>Data sent to mqtt:</b> <br><br> [msg] : " + data + "<br><br> <a href='/'><button>Back</button></a> <meta http-equiv='refresh' content='3;url=/' />"


# Me conecto al Rabbit y envio el mensaje que fue creado en el formulario, cierro la conexión y envio un mensaje.
def send_mqtt_msg(queue, routing_key, data):
  redentials  = pika.PlainCredentials(mqttuser, mqttpass)
  parameters  = pika.ConnectionParameters(host=mqtthost,port=mqttport,virtual_host=mqttvhost,credentials=credentials,connection_attempts=5, retry_delay=5)
  connection  = pika.BlockingConnection(parameters)
  channel     = connection.channel()
  channel.queue_declare(queue=queue, durable=True)
  channel.basic_publish(exchange='', routing_key=routing_key, body=data)
  connection.close() 
  sendmsg('-   *[Producer] Data sent mqtt message to queue: '+queue)


# Funcion para exponer metricas custom de esta app.
def monitoring():
  metric_info = Info('producer_version', 'build version of producer')
  metric_info.info({'name':'producer', 'version': '1.0.0', 'owner': 'jpradoar',})
  start_http_server(9090)


def main():
  sendmsg('-   *[Producer] Started')
  app.run(host='0.0.0.0', port=5000, debug=False)
  


if __name__ == '__main__':
  # uso el trheading para exponer cada funcion en un hilo separado. 
  Thread(target = main).start()
  Thread(target = monitoring).start()
