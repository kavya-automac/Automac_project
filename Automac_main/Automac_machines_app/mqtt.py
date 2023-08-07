import os
from datetime import time
from django.apps import apps
import paho.mqtt.client as mqtt
from django.conf import settings
import json
#
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
    # print('payload1',payload1)

    multi_topic_file.all_topics(payload1)



    from . import physical_keys_values

    data=physical_keys_values.test_fun(payload1)
    channel_layer = get_channel_layer()  # get default channel layer  RedisChannelLayer(hosts=[{'address': 'redis://65.2.3.42:6379'}])
    async_to_sync(channel_layer.group_send)("mqtt_data", {"type": "chat.message", "text": data})

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
client.connect(
   host=settings.MQTT_SERVER,
   port=settings.MQTT_PORT,
   keepalive=settings.MQTT_KEEPALIVE
)

#
#
# def on_connect_1(client_1, userdata, flags, rc):
#    if rc == 0:
#        print('Connected successfully on aws')
#        client_1.subscribe('Maithri/Device_7inch')
#    else:
#        print('Bad connection. Code:', rc)
#
#
#
#
#
# def on_message_1(client_1, userdata, msg):
#     # print("on_message")
#     # print(f'Received message on topic: {msg.topic} with payload: {msg.payload}')
#
#     payload1 = msg.payload.decode()  # Assuming the payload is a string
#     # print('payload1',payload1)
#
#     multi_topic_file.all_topics(payload1)
#
#
#
#     from . import physical_keys_values
#
#     data=physical_keys_values.test_fun(payload1)
#     channel_layer = get_channel_layer()  # get default channel layer  RedisChannelLayer(hosts=[{'address': 'redis://65.2.3.42:6379'}])
#     async_to_sync(channel_layer.group_send)("mqtt_data", {"type": "chat.message", "text": data})
#
# client_1 = mqtt.Client()
# client_1.on_connect = on_connect_1
# client_1.on_message = on_message_1
# # client_1.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
# client_1.tls_set(settings.CAPATH, certfile=settings.CERTPATH, keyfile=settings.KEYPATH,
#                     cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
# client_1.connect(
#
#    host=settings.AWSHOST,
#    port=settings.AWSPORT,
#    keepalive=settings.MQTT_KEEPALIVE
# )
#
