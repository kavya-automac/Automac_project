from datetime import time
from django.apps import apps
import paho.mqtt.client as mqtt
from django.conf import settings
import json
#
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from . import multi_topic_file
print('mqtt')

def on_connect(client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully')
       client.subscribe('maithri/abu_dabhi')
   else:
       print('Bad connection. Code:', rc)



def on_message(client, userdata, msg):
    # print("on_message")
    # print(f'Received message on topic: {msg.topic} with payload: {msg.payload}')


    payload1 = msg.payload.decode()  # Assuming the payload is a string


    multi_topic_file.all_topics(payload1)

    from . import test_file

    data=test_file.test_fun(payload1)


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


