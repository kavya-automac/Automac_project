from datetime import time
from django.apps import apps
import paho.mqtt.client as mqtt
from django.conf import settings
import json

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

print('mqtt')

def on_connect(client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully')
       client.subscribe('Topic_name')
   else:
       print('Bad connection. Code:', rc)



def on_message(client, userdata, msg):
    print("on_message")
    print(f'Received message on topic: {msg.topic} with payload: {msg.payload}')


    payload1 = msg.payload.decode()  # Assuming the payload is a string

    channel_layer = get_channel_layer()  # get default channel layer  RedisChannelLayer(hosts=[{'address': 'redis://65.2.3.42:6379'}])
    async_to_sync(channel_layer.group_send)("mqtt_data", {"type": "chat.message", "text": payload1})


    payload = json.loads(payload1)

    # Extract the data from the JSON payload
    timestamp = payload['timestamp']
    machine_id = payload['machine_id']
    machine_location = payload['machine_location']
    digital_input = payload['digital_input']
    digital_output = payload['digital_output']
    analog_input = payload['analog_input']
    analog_output = payload['analog_output']



    MachineDetails = apps.get_model('Automac_machines_app', 'MachineDetails')

    # Create an instance of the SensorData model
    sensor_data = MachineDetails(
       # timestamp=timezone.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f'),
       timestamp=timestamp,
       machine_id=machine_id,
       machine_location=machine_location,
       digital_input=digital_input,
       digital_output=digital_output,
       analog_input=analog_input,
       analog_output=analog_output
    )

    # Save the instance to the database
    sensor_data.save()



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
client.connect(
   host=settings.MQTT_SERVER,
   port=settings.MQTT_PORT,
   keepalive=settings.MQTT_KEEPALIVE
)


