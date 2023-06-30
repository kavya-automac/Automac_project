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

    payload = json.loads(payload1)

    digital_input_keys = data2[0]['digital_input']
    digital_output_keys = data2[0]['digital_output']
    analog_input_keys = data2[0]['analog_input']
    analog_output_keys = data2[0]['analog_output']
    digital_input = [payload['Temperature'], payload['Humidity'], payload['LP1'], payload['LP2'], payload['HP1'],
       payload['HP2'], payload['Dosing'], payload['3PhasePreventer']]

    digital_output = [payload['Compressor_1'], payload['Compressor_2'], payload['Pump1'], payload['Pump2'],
                                              payload['Pump3']]

    analog_input = []
    analog_output = [payload['Flow']]

    channels_data_input = dict(zip(digital_input_keys, digital_input))
    # print('channels_data_input',channels_data_input)
    channels_data_output = dict(zip(digital_output_keys, digital_output))
    a_channels_data_input = dict(zip(analog_input_keys, analog_input))
    a_channels_data_output = dict(zip(analog_output_keys, analog_output))


    result = {
        'channels_data_input': channels_data_input, 'channels_data_output': channels_data_output,'a_channels_data_input':a_channels_data_input,'a_channels_data_output':a_channels_data_output
    }
    res=json.dumps(result)
    # print(type(res))

    return res


