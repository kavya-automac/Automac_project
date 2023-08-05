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
    digital_input = [payload['LP1'], payload['LP2'], payload['HP1'],payload['HP2'], payload['Dosing'], payload['3PhasePreventer']]

    digital_output = [payload['Compressor_1'], payload['Compressor_2'], payload['Pump1'], payload['Pump2'],
                                              payload['Pump3']]

    analog_input = [payload['Temperature'], payload['Humidity']]
    analog_output = [payload['Flow']]
    machine_id=data2[0]['machine_id']
    machine_name=data2[0]['machine_name']
    # 1
    # digital_data_input = dict(zip(digital_input_keys, digital_input))
    #
    # # print('channels_data_input',channels_data_input)
    # digital_data_output = dict(zip(digital_output_keys, digital_output))
    # analog_data_input = dict(zip(analog_input_keys, analog_input))
    # analog_data_output = dict(zip(analog_output_keys, analog_output))

    data = [
               {"name": key, "value": value} for key, value in zip(digital_input_keys, digital_input)
           ] + [
               {"name": key, "value": value} for key, value in zip(digital_output_keys, digital_output)
           ] + [
               {"name": key, "value": value} for key, value in zip(analog_input_keys, analog_input)
           ] + [
               {"name": key, "value": value} for key, value in zip(analog_output_keys, analog_output)
           ]
    print('data',data)





    result = {'machine_id': machine_id, 'machine_name': machine_name, "data":data
              }

    # result = {'machine_id':machine_id,'machine_name':machine_name,'digital_input': digital_data_input,
    #           'digital_output': digital_data_output,'analog_input':analog_data_input,
    #           'analog_output':analog_data_output
    # }

    result['db_timestamp']=payload['timestamp']
    # print('mmmmmmm',type(result))

    res=json.dumps(result)
    # print('res',res)


    # channel_layer = get_channel_layer()  # get default channel layer  RedisChannelLayer(hosts=[{'address': 'redis://65.2.3.42:6379'}])
    # async_to_sync(channel_layer.group_send)("mqtt_data", {"type": "chat.message", "text": res})
    #

    return res


