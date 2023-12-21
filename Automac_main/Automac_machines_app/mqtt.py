import os
from django.apps import apps
import paho.mqtt.client as mqtt
from django.conf import settings
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
       client.subscribe('demo_app')
       client.subscribe('CSD')
       client.subscribe('websocket_data')
       client.subscribe('Maithri_test')

   else:
       print('Bad connection. Code:', rc)

def on_message(client, userdata, msg):
    # print("on_message")
    # print(f'Received message on topic: {msg.topic} with payload: {msg.payload}')

    mqtt_machines_data = msg.payload.decode()  # Assuming the payload is a string
    # payload_json = json.loads(mqtt_machines_data)
    topic=msg.topic
    # print('mqtt_machines_data',msg.topic)
    # print('timestamp :', payload_json['timestamp'])
    # print('machineid :', payload_json['info']['mid'])



    multi_topic_file.all_topics(mqtt_machines_data,topic)

    if topic =='maithri/abu_dabhi' or topic =='Topic_name':
        from . import physical_keys_values
        physical_keys_values.mqtt_data_to_channels(mqtt_machines_data)
    if topic == 'demo_app'or topic == "CSD" and topic == "Maithri_test":
        from . import physical_keys_values


        physical_keys_values.demo_app_to_channels(mqtt_machines_data)
    if topic == "websocket_data":
        from . import physical_keys_values

        physical_keys_values.demo_app_to_channels(mqtt_machines_data)

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
       client_1.subscribe('Maithri_test')
   else:
       print('Bad connection. Code:', rc)

def on_message_1(client_1, userdata, msg):
    # print("on_message")
    # print(f'Received message on topic: {msg.topic} with payload: {msg.payload}')

    mqtt_machines_data = msg.payload.decode()  # Assuming the payload is a string
    topic=msg.topic
    print('aws data MID004',mqtt_machines_data)
    # print('payload1',msg.topic)


    multi_topic_file.all_topics(mqtt_machines_data,topic)
    # print('topicname',payload1.Topic)



    # from . import physical_keys_values
    if topic =='Maithri/Device_7inch':
        from . import physical_keys_values

        physical_keys_values.Device_7inch(mqtt_machines_data)
    if topic == "Maithri_test":
        from . import physical_keys_values


        physical_keys_values.demo_app_to_channels(mqtt_machines_data)



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




#--------------------------------------------------testingg--------------------

#
#
# def on_connect_2(client_2, userdata, flags, rc):
#    if rc == 0:
#        print('Connected successfully on hive(testingggg)')
#        client_2.subscribe('demo_app')
#    else:
#        print('Bad connection. Code:', rc)
#
# def on_message_2(client_2, userdata, msg):
#     # print("on_message")
#     # print(f'Received message on topic: {msg.topic} with payload: {msg.payload}')
#
#     mqtt_machines_data = msg.payload.decode()  # Assuming the payload is a string
#     print('mqtt_machines_data',mqtt_machines_data)
#     topic=msg.topic
#
#     multi_topic_file.all_topics(mqtt_machines_data,topic)
#
#     if topic =='demo_app':
#         from . import physical_keys_values
#
#         physical_keys_values.demo_app_to_channels(mqtt_machines_data)
#
#
#
#
# client_2 = mqtt.Client()
# client_2.on_connect = on_connect_2
# client_2.on_message = on_message_2
# client_2.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
# client_2.connect(
#    host=settings.MQTT_SERVER,
#    port=settings.MQTT_PORT,
#    keepalive=settings.MQTT_KEEPALIVE
# )
