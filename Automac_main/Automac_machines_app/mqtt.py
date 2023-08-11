import os
from datetime import time
from django.apps import apps
import paho.mqtt.client as mqtt
from django.conf import settings
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from . import multi_topic_file
import ssl

print('mqtt')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Automac_main.settings')

a=settings.CAPATH
print('s..........',a)

def on_connect(client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully on hive')
       client.subscribe('maithri/abu_dabhi')
       client.subscribe('Topic_name')
   else:
       print('Bad connection. Code:', rc)

def on_message(client, userdata, msg):
    # print("on_message")
    # print(f'Received message on topic: {msg.topic} with payload: {msg.payload}')

    payload1 = msg.payload.decode()  # Assuming the payload is a string
    payload_json = json.loads(payload1)
    topic=msg.topic
    print('payload1',msg.topic)
    print('timestamp :', payload_json['timestamp'])
    print('machineid :', payload_json['info']['mid'])

    multi_topic_file.all_topics(payload1,topic)

    if topic =='maithri/abu_dabhi' or topic =='Topic_name':
        from . import physical_keys_values
        physical_keys_values.physical_k_v_combined(payload1)
    else:
        pass

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
client.connect(
   host=settings.MQTT_SERVER,
   port=settings.MQTT_PORT,
   keepalive=settings.MQTT_KEEPALIVE
)


# aws connection  MID004-----------------------------------------------

def on_connect_1(client_1, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully on aws')
       client_1.subscribe('Maithri/Device_7inch')
   else:
       print('Bad connection. Code:', rc)

def on_message_1(client_1, userdata, msg):
    # print("on_message")
    # print(f'Received message on topic: {msg.topic} with payload: {msg.payload}')

    payload1 = msg.payload.decode()  # Assuming the payload is a string
    topic=msg.topic
    # print('payload1',payload1)
    print('payload1',msg.topic)


    multi_topic_file.all_topics(payload1,topic)
    # print('topicname',payload1.Topic)



    # from . import physical_keys_values
    if topic =='Maithri/Device_7inch':
        from . import physical_keys_values

        physical_keys_values.Device_7inch(payload1)


client_1 = mqtt.Client()
client_1.on_connect = on_connect_1
client_1.on_message = on_message_1
# client_1.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
client_1.tls_set(settings.CAPATH, certfile=settings.CERTPATH, keyfile=settings.KEYPATH,
                    cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
client_1.connect(

   host=settings.AWSHOST,
   port=settings.AWSPORT,
   keepalive=settings.MQTT_KEEPALIVE
)
