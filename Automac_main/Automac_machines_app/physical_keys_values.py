import json
from Automac_app.models import Machines_List
from Automac_app.serializers import usermachineSerializer
# from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework.response import Response


def test_fun(payload1):
    payload = json.loads(payload1)

    # Extract machine_id from the payload
    machine_id = payload['info']['mid']

    # Query the Machines_List model to get data for the specific machine_id
    user_data = Machines_List.objects.filter(machine_id=machine_id)
    # user_data = Machines_List.objects.filter(machine_id=machine_id)
    print('user_dataaaaaaaaaa',user_data)
    # query_string_bytes = self.scope['query_string']
    # query_string = query_string_bytes.decode('utf-8')
    # print('qqqq', query_string)

    if user_data.exists():


        # self.scope['query_string']['machine_id']
        user_serializer = usermachineSerializer(user_data.first())  # Get a single instance
        data2 = user_serializer.data

        # Extract keys for digital_input, digital_output, analog_input, and analog_output
        digital_input_keys = data2['digital_input']
        digital_output_keys = data2['digital_output']
        analog_input_keys = data2['analog_input']
        analog_output_keys = data2['analog_output']

        # Extract values from the payload using the corresponding keys
        digital_input = [payload.get('LP1'), payload.get('LP2'), payload.get('HP1'), payload.get('HP2'),
                         payload.get('Dosing'), payload.get('3PhasePreventer')]
        digital_output = [payload.get('Compressor_1'),  payload.get('Pump'),payload.get('Compressor_2'), payload.get('Pump1'),
                          payload.get('Pump2'), payload.get('Pump3')]
        analog_input = [payload.get('Temperature'), payload.get('Humidity')]
        analog_output = [payload.get('Flow')]

        # Create dictionaries for data to be sent
        digital_data_input = [{"name": key, "value": str(value)} for key, value in zip(digital_input_keys, digital_input)]
        digital_data_output = [{"name": key, "value": str(value)} for key, value in zip(digital_output_keys, digital_output)]
        analog_data_input = [{"name": key, "value": str(value)} for key, value in zip(analog_input_keys, analog_input)]
        analog_data_output = [{"name": key, "value": str(value)} for key, value in zip(analog_output_keys, analog_output)]

        # Construct the final result dictionary
        result = {
            'machine_id': machine_id,
            'machine_name': data2['machine_name'],
            'digital_input': digital_data_input,
            'digital_output': digital_data_output,
            'analog_input': analog_data_input,
            'analog_output': analog_data_output,
            'db_timestamp': payload['timestamp']
        }

        # Convert the result dictionary to a JSON string
        res = json.dumps(result)
        channel_layer = get_channel_layer()  # get default channel layer  RedisChannelLayer(hosts=[{'address': 'redis://65.2.3.42:6379'}])
        # async_to_sync(channel_layer.group_send)(user_data, {"type": "chat.message", "text": res})
        # print('channel_layer',channel_layer)
        async_to_sync(channel_layer.group_send)(machine_id, {"type": "chat.message", "text": res})

        # return res
    else:
        return None  # Handle the case where machine_id doesn't exist


#
# for key in digital_output_keys:
#     value = payload.get(key)
#     digital_output.append({"name": key, "value": value})

# ====================================================================================================
# def test_fun(payload1):
#     # a=payload1['info']['mid']
#     # print('aaaaaaa',a)
#     # u_data=Machines_List.objects.filter(machine_id=machine_id)
#     payload = json.loads(payload1)
#     machine_id = payload['info']['mid']  # Extract the machine_id
#     print('mmmmmmmmmm', machine_id)
#     user_data = Machines_List.objects.filter(machine_id=machine_id)
#
#     # user_data = Machines_List.objects.all()
#     user_serializer = usermachineSerializer(user_data, many=True)
#     data2 = user_serializer.data
#     print('data2',data2)
#
#
#     # print('payload',payload)
#
#     digital_input_keys = data2[0]['digital_input']
#     digital_output_keys = data2[0]['digital_output']
#     analog_input_keys = data2[0]['analog_input']
#     analog_output_keys = data2[0]['analog_output']
#     digital_input = [payload.get('LP1'), payload.get('LP2'), payload.get('HP1'), payload.get('HP2'),
#                      payload.get('Dosing'), payload.get('3PhasePreventer')]
#     digital_output = [payload.get('Compressor_1'), payload.get('Compressor_2'), payload.get('Pump1'),
#                       payload.get('Pump2'), payload.get('Pump3')]
#     analog_input = [payload.get('Temperature'), payload.get('Humidity')]
#     analog_output = [payload.get('Flow')]
#     machine_id=data2[0]['machine_id']
#     machine_name=data2[0]['machine_name']
#     # 1
#     # digital_data_input = dict(zip(digital_input_keys, digital_input))
#     #
#     # # print('channels_data_input',channels_data_input)
#     # digital_data_output = dict(zip(digital_output_keys, digital_output))
#     # analog_data_input = dict(zip(analog_input_keys, analog_input))
#     # analog_data_output = dict(zip(analog_output_keys, analog_output))
#
#     # data = [
#     #            {"name": key, "value": value} for key, value in zip(digital_input_keys, digital_input)
#     #        ] + [
#     #            {"name": key, "value": value} for key, value in zip(digital_output_keys, digital_output)
#     #        ] + [
#     #            {"name": key, "value": value} for key, value in zip(analog_input_keys, analog_input)
#     #        ] + [
#     #            {"name": key, "value": value} for key, value in zip(analog_output_keys, analog_output)
#     #        ]
#     # print('data',data)
#
#     digital_data_input=[{"name": key, "value": value} for key, value in zip(digital_input_keys, digital_input)]
#
#     digital_data_output=[{"name": key, "value": value} for key, value in zip(digital_output_keys, digital_output)]
#     analog_data_input=[{"name": key, "value": value} for key, value in zip(analog_input_keys, analog_input)]
#
#     analog_data_output=[{"name": key, "value": value} for key, value in zip(analog_output_keys, analog_output)]
#
#
#
#
#
#     result = {'machine_id':machine_id,'machine_name':machine_name,'digital_input': digital_data_input,
#               'digital_output': digital_data_output,'analog_input':analog_data_input,
#               'analog_output':analog_data_output
#     }
#
#     result['db_timestamp']=payload['timestamp']
#     # print('mmmmmmm',type(result))
#
#     res=json.dumps(result)
#
#
#     return res
#



# -------------------------------------------------------------------------------------------
































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
