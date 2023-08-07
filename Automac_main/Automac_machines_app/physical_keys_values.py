import json
from Automac_app.models import Machines_List
from Automac_app.serializers import usermachineSerializer
# from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework.response import Response


def test_fun(payload1):
    user_data = Machines_List.objects.all()
    user_serializer = usermachineSerializer(user_data, many=True)
    data2 = user_serializer.data
    # print('data2',data2)

    payload = json.loads(payload1)
    # print('payload',payload)

    digital_input_keys = data2[0]['digital_input']
    digital_output_keys = data2[0]['digital_output']
    analog_input_keys = data2[0]['analog_input']
    analog_output_keys = data2[0]['analog_output']
    digital_input = [payload.get('LP1'), payload.get('LP2'), payload.get('HP1'), payload.get('HP2'),
                     payload.get('Dosing'), payload.get('3PhasePreventer')]
    digital_output = [payload.get('Compressor_1'), payload.get('Compressor_2'), payload.get('Pump1'),
                      payload.get('Pump2'), payload.get('Pump3')]
    analog_input = [payload.get('Temperature'), payload.get('Humidity')]
    analog_output = [payload.get('Flow')]
    machine_id=data2[0]['machine_id']
    machine_name=data2[0]['machine_name']
    # 1
    # digital_data_input = dict(zip(digital_input_keys, digital_input))
    #
    # # print('channels_data_input',channels_data_input)
    # digital_data_output = dict(zip(digital_output_keys, digital_output))
    # analog_data_input = dict(zip(analog_input_keys, analog_input))
    # analog_data_output = dict(zip(analog_output_keys, analog_output))

    # data = [
    #            {"name": key, "value": value} for key, value in zip(digital_input_keys, digital_input)
    #        ] + [
    #            {"name": key, "value": value} for key, value in zip(digital_output_keys, digital_output)
    #        ] + [
    #            {"name": key, "value": value} for key, value in zip(analog_input_keys, analog_input)
    #        ] + [
    #            {"name": key, "value": value} for key, value in zip(analog_output_keys, analog_output)
    #        ]
    # print('data',data)

    digital_data_input=[{"name": key, "value": value} for key, value in zip(digital_input_keys, digital_input)]

    digital_data_output=[{"name": key, "value": value} for key, value in zip(digital_output_keys, digital_output)]
    analog_data_input=[{"name": key, "value": value} for key, value in zip(analog_input_keys, analog_input)]

    analog_data_output=[{"name": key, "value": value} for key, value in zip(analog_output_keys, analog_output)]



    # result = {'machine_id': machine_id, 'machine_name': machine_name, "data":data
    #           }

    result = {'machine_id':machine_id,'machine_name':machine_name,'digital_input': digital_data_input,
              'digital_output': digital_data_output,'analog_input':analog_data_input,
              'analog_output':analog_data_output
    }

    result['db_timestamp']=payload['timestamp']
    # print('mmmmmmm',type(result))

    res=json.dumps(result)
    # print('res',res)


    # channel_layer = get_channel_layer()  # get default channel layer  RedisChannelLayer(hosts=[{'address': 'redis://65.2.3.42:6379'}])
    # async_to_sync(channel_layer.group_send)("mqtt_data", {"type": "chat.message", "text": res})


    return res
# def test_fun(payload1):
#     user_data = Machines_List.objects.all()
#     user_serializer = usermachineSerializer(user_data, many=True)
#     data2 = user_serializer.data
#
#     payload = json.loads(payload1)
#
#     # results = []  # Create a list to store individual results for each key
#
#     for keys in data2:
#         print('jjjj',keys['digital_input'])
#         print('lllllllll',keys['machine_name'])
#         digital_input_keys = keys['digital_input']
#         digital_output_keys = keys['digital_output']
#         analog_input_keys = keys['analog_input']
#         analog_output_keys = keys['analog_output']
#
#         digital_input = [payload.get('LP1'), payload.get('LP2'), payload.get('HP1'), payload.get('HP2'),
#                          payload.get('Dosing'), payload.get('3PhasePreventer')]
#         digital_output = [payload.get('Compressor_1'), payload.get('Compressor_2'), payload.get('Pump1'),
#                           payload.get('Pump2'), payload.get('Pump3')]
#         analog_input = [payload.get('Temperature'), payload.get('Humidity')]
#         analog_output = [payload.get('Flow')]
#
#         machine_id = keys['machine_id']
#         machine_name = keys['machine_name']
#
#         digital_data_input = [{"name": key, "value": value} for key, value in zip(digital_input_keys, digital_input)]
#         digital_data_output = [{"name": key, "value": value} for key, value in zip(digital_output_keys, digital_output)]
#         analog_data_input = [{"name": key, "value": value} for key, value in zip(analog_input_keys, analog_input)]
#         analog_data_output = [{"name": key, "value": value} for key, value in zip(analog_output_keys, analog_output)]
#
#         result = {
#             'machine_id': machine_id,
#             'machine_name': machine_name,
#             'digital_input': digital_data_input,
#             'digital_output': digital_data_output,
#             'analog_input': analog_data_input,
#             'analog_output': analog_data_output,
#             'db_timestamp': payload['timestamp']
#         }
#
#         # results.append(result)  # Add the result for this key to the list
#
#     return json.dumps(result)  # Return the list of results as a JSON string

 # 1
    # digital_data_input = dict(zip(digital_input_keys, digital_input))
    #
    # # print('channels_data_input',channels_data_input)
    # digital_data_output = dict(zip(digital_output_keys, digital_output))
    # analog_data_input = dict(zip(analog_input_keys, analog_input))
    # analog_data_output = dict(zip(analog_output_keys, analog_output))

    # data = [
    #            {"name": key, "value": value} for key, value in zip(digital_input_keys, digital_input)
    #        ] + [
    #            {"name": key, "value": value} for key, value in zip(digital_output_keys, digital_output)
    #        ] + [
    #            {"name": key, "value": value} for key, value in zip(analog_input_keys, analog_input)
    #        ] + [
    #            {"name": key, "value": value} for key, value in zip(analog_output_keys, analog_output)
    #        ]
    # print('data',data)
