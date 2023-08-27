import json
from Automac_app.models import Machines_List,IO_List
from Automac_app.serializers import usermachineSerializer,IO_list_serializer
# from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import JsonResponse
from rest_framework.response import Response

#
# def mqtt_data_to_channels(payload1):
#     # print('hhhh')
#     payload = json.loads(payload1)
#
#     # Extract machine_id from the payload
#     machine_id = payload['info']['mid']
#
#     # Query the Machines_List model to get data for the specific machine_id
#     user_data = Machines_List.objects.filter(machine_id=machine_id)
#     # user_data = Machines_List.objects.filter(machine_id=machine_id)
#     print('user_dataaaaaaaaaa',user_data)
#     # query_string_bytes = self.scope['query_string']
#     # query_string = query_string_bytes.decode('utf-8')
#     # print('qqqq', query_string)
#
#     if user_data.exists():
#
#
#         # self.scope['query_string']['machine_id']
#         user_serializer = usermachineSerializer(user_data.first())  # Get a single instance
#         data2 = user_serializer.data
#
#         # Extract keys for digital_input, digital_output, analog_input, and analog_output
#         digital_input_keys = data2['digital_input']
#         digital_output_keys = data2['digital_output']
#         analog_input_keys = data2['analog_input']
#         analog_output_keys = data2['analog_output']
#
#         # Extract values from the payload using the corresponding keys
#         digital_input = [payload.get('LP1'), payload.get('LP2'), payload.get('HP1'), payload.get('HP2'),
#                          payload.get('Dosing'), payload.get('3PhasePreventer')]
#         digital_output = [payload.get('Compressor_1'),payload.get('Compressor_2'), payload.get('Pump1'),
#                           payload.get('Pump2'), payload.get('Pump3')]
#         analog_input = [payload.get('Temperature'), payload.get('Humidity')]
#         analog_output = [payload.get('Flow')]
#
#         # Create dictionaries for data to be sent
#         digital_data_input = [{"name": key, "value": str(value)} for key, value in zip(digital_input_keys, digital_input)]
#         digital_data_output = [{"name": key, "value": str(value)} for key, value in zip(digital_output_keys, digital_output)]
#         analog_data_input = [{"name": key, "value": str(value)} for key, value in zip(analog_input_keys, analog_input)]
#         analog_data_output = [{"name": key, "value": str(value)} for key, value in zip(analog_output_keys, analog_output)]
#
#         # Construct the final result dictionary
#         result = {
#             'machine_id': machine_id,
#             'machine_name': data2['machine_name'],
#             'digital_input': digital_data_input,
#             'digital_output': digital_data_output,
#             'analog_input': analog_data_input,
#             'analog_output': analog_data_output,
#             'db_timestamp': payload['timestamp']
#         }
#
#         # Convert the result dictionary to a JSON string
#         res = json.dumps(result)
#         channel_layer = get_channel_layer()  # get default channel layer  RedisChannelLayer(hosts=[{'address': 'redis://65.2.3.42:6379'}])
#         # async_to_sync(channel_layer.group_send)(user_data, {"type": "chat.message", "text": res})
#         # print('channel_layer',channel_layer)
#         async_to_sync(channel_layer.group_send)(machine_id, {"type": "chat.message", "text": res})
#
#         # return res
#     else:
#         return None  # Handle the case where machine_id doesn't exist

#
#
# def Device_7inch(payload1):
#     # print('kkk')
#
#     payload = json.loads(payload1)
#
#     # Extract machine_id from the payload
#     machine_id = payload['info']['mid']
#
#     # Query the Machines_List model to get data for the specific machine_id
#     user_data2 = Machines_List.objects.filter(machine_id=machine_id)
#     # user_data = Machines_List.objects.filter(machine_id=machine_id)
#     print('user_dataaaaaaaaaa',user_data2)
#     # query_string_bytes = self.scope['query_string']
#     # query_string = query_string_bytes.decode('utf-8')
#     # print('qqqq', query_string)
#
#     if user_data2.exists():
#
#
#         # self.scope['query_string']['machine_id']
#         user_serializer = usermachineSerializer(user_data2.first())  # Get a single instance
#         data2 = user_serializer.data
#
#         # Extract keys for digital_input, digital_output, analog_input, and analog_output
#         digital_input_keys = data2['digital_input']
#         print('digital_input_keys',digital_input_keys)
#         digital_output_keys = data2['digital_output']
#         analog_input_keys = data2['analog_input']
#         analog_output_keys = data2['analog_output']
#
#         # Extract values from the payload using the corresponding keys
#         digital_input = [payload.get('Dosing')]
#         digital_output = [payload.get('Compressor_1'),  payload.get('Pump')]
#         analog_input = [payload.get('Temperature'), payload.get('Humidity')]
#         analog_output = [payload.get('Flow')]
#
#         # Create dictionaries for data to be sent
#         digital_data_input = [{"name": key, "value": str(value)} for key, value in zip(digital_input_keys, digital_input)]
#         digital_data_output = [{"name": key, "value": str(value)} for key, value in zip(digital_output_keys, digital_output)]
#         analog_data_input = [{"name": key, "value": str(value)} for key, value in zip(analog_input_keys, analog_input)]
#         analog_data_output = [{"name": key, "value": str(value)} for key, value in zip(analog_output_keys, analog_output)]
#
#         # Construct the final result dictionary
#         result = {
#             'machine_id': machine_id,
#             'machine_name': data2['machine_name'],
#             'digital_input': digital_data_input,
#             'digital_output': digital_data_output,
#             'analog_input': analog_data_input,
#             'analog_output': analog_data_output,
#             'db_timestamp': payload['timestamp']
#         }
#
#         # Convert the result dictionary to a JSON string
#         res = json.dumps(result)
#         channel_layer = get_channel_layer()  # get default channel layer  RedisChannelLayer(hosts=[{'address': 'redis://65.2.3.42:6379'}])
#         # async_to_sync(channel_layer.group_send)(user_data, {"type": "chat.message", "text": res})
#         # print('channel_layer',channel_layer)
#         async_to_sync(channel_layer.group_send)(machine_id, {"type": "chat.message", "text": res})
#
#         # return res
#     else:
#         return None  # Handle the case where machine_id doesn't exist
#



def mqtt_data_to_channels(payload1):
    # print('hhhh')

    payload = json.loads(payload1)
    print('payload 7inch',payload)
    # Extract machine_id from the payload
    machine_id = payload['info']['mid']
    print('machineeeeeeeeee',machine_id)

    # Query the Machines_List model to get data for the specific machine_id
    # machine = Machines_List.objects.get(machine_id=machine_id)
    # print('machine',machine)

    try:
        machine = Machines_List.objects.get(machine_id=machine_id)
    except Machines_List.DoesNotExist:
        error_message = "Please enter a valid machine_id."
        return JsonResponse({"status": error_message}, status=400)  # Return an error response

    # self.scope['query_string']['machine_id']
    # user_serializer = usermachineSerializer(machine.first())  # Get a single instance
    # data2 = user_serializer.data

    # Extract keys for digital_input, digital_output, analog_input, and analog_output
    input_output_data = IO_List.objects.filter(machine_id=machine.id).order_by('id')
    print('input_output_data', input_output_data)
    input_output_data_serializer = IO_list_serializer(input_output_data, many=True)
    print('input_output_data_serializer', input_output_data_serializer.data)
    input_output_data_serializer_data = input_output_data_serializer.data


    digital_input_keys = []
    digital_output_keys = []
    analog_input_keys = []
    analog_output_keys = []
    for i in range(len(input_output_data)):
        if input_output_data_serializer_data[i]['IO_type'] == "digital_input":
            digital_input_keys.append(input_output_data_serializer_data[i]['IO_name'])

        if input_output_data_serializer_data[i]['IO_type'] == "digital_output":
            digital_output_keys.append(input_output_data_serializer_data[i]['IO_name'])

        if input_output_data_serializer_data[i]['IO_type'] == "analog_input":
            analog_input_keys.append(input_output_data_serializer_data[i]['IO_name'])
        if input_output_data_serializer_data[i]['IO_type'] == "analog_output":
            analog_output_keys.append(input_output_data_serializer_data[i]['IO_name'])

    # Extract values from the payload using the corresponding keys
    digital_input = [payload.get('LP1'), payload.get('LP2'), payload.get('HP1'), payload.get('HP2'),
                                              payload.get('Dosing'), payload.get('3PhasePreventer')]
    digital_output = [payload.get('Compressor_1'),payload.get('Compressor_2'), payload.get('Pump1'),
                                               payload.get('Pump2'), payload.get('Pump3')]
    analog_input = [payload.get('Temperature'), payload.get('Humidity')]
    analog_output = [payload.get('Flow')]

    digital_keyvalue_input_data = []

    for key, value in zip(digital_input_keys, digital_input):
        value_str = "On" if value else "Off"
        color = None
        for i in range(len(input_output_data)):
            if input_output_data_serializer_data[i]['IO_type'] == "digital_input" and \
                    input_output_data_serializer_data[i]['IO_name'] == key:
                db_color = input_output_data_serializer_data[i]['IO_color']
                color = db_color[0] if value else db_color[1]
                break  # Exit loop once the correct key is found
            else:
                pass

        digital_keyvalue_input_data.append({"name": key, "value": value_str, "color": color})
    print('digital_keyvalue_input_data', digital_keyvalue_input_data)

    digital_keyvalue_output_data = []

    for key, value in zip(digital_output_keys, digital_output):
        value_str = "On" if value else "Off"  # Convert boolean to "On" or "Off"
        color = None
        for i in range(len(input_output_data)):
            if input_output_data_serializer_data[i]['IO_type'] == "digital_output" and \
                    input_output_data_serializer_data[i]['IO_name'] == key:
                db_color = input_output_data_serializer_data[i]['IO_color']
                color = db_color[0] if value else db_color[1]
                break  # Exit loop once the correct key is found
            else:
                pass

        digital_keyvalue_output_data.append({"name": key, "value": value_str, "color": color})
    print('digital_keyvalue_output_data', digital_keyvalue_output_data)

    analog_keyvalue_input_data = []
    for key, value in zip(analog_input_keys, analog_input):
        db_unit = None
        for i in range(len(input_output_data)):
            if input_output_data_serializer_data[i]['IO_type'] == "analog_input" and \
                    input_output_data_serializer_data[i]['IO_name'] == key:
                db_unit = input_output_data_serializer_data[i]['IO_Unit']
                color = input_output_data_serializer_data[i]['IO_color'][0]
                break  # Exit loop once the correct key is found
            else:
                pass

        analog_keyvalue_input_data.append({"name": key, "value": str(value), "color": color, "unit": db_unit})
    print('analog_keyvalue_input_data', analog_keyvalue_input_data)

    analog_keyvalue_output_data = []
    for key, value in zip(analog_output_keys, analog_output):
        db_unit = None
        for i in range(len(input_output_data)):
            if input_output_data_serializer_data[i]['IO_type'] == "analog_output" and \
                    input_output_data_serializer_data[i]['IO_name'] == key:
                db_unit = input_output_data_serializer_data[i]['IO_Unit']
                color = input_output_data_serializer_data[i]['IO_color'][0]

                break  # Exit loop once the correct key is found
            else:
                pass

        analog_keyvalue_output_data.append({"name": key, "value": str(value), "color": color, "unit": db_unit})
    print('analog_keyvalue_output_data', analog_keyvalue_output_data)

    # Create dictionaries for data to be sent

    # Construct the final result dictionary
    result = {
        'machine_id': machine_id,
        'machine_name': machine.machine_name,
        'digital_input': digital_keyvalue_input_data,
        'digital_output': digital_keyvalue_output_data,
        'analog_input': analog_keyvalue_input_data,
        'analog_output': analog_keyvalue_output_data,
        'db_timestamp': payload['timestamp']
    }

    # Convert the result dictionary to a JSON string
    res = json.dumps(result)
    channel_layer = get_channel_layer()  # get default channel layer  RedisChannelLayer(hosts=[{'address': 'redis://65.2.3.42:6379'}])
    # async_to_sync(channel_layer.group_send)(user_data, {"type": "chat.message", "text": res})
    # print('channel_layer',channel_layer)
    async_to_sync(channel_layer.group_send)(machine_id, {"type": "chat.message", "text": res})








def Device_7inch(payload1):
    # print('kkk')

    payload = json.loads(payload1)
    print('payload 7inch',payload)
    # Extract machine_id from the payload
    machine_id = payload['info']['mid']
    print('machineeeeeeeeee',machine_id)

    # Query the Machines_List model to get data for the specific machine_id
    # machine = Machines_List.objects.get(machine_id=machine_id)
    # print('machine',machine)

    try:
        machine = Machines_List.objects.get(machine_id=machine_id)
    except Machines_List.DoesNotExist:
        error_message = "Please enter a valid machine_id."
        return JsonResponse({"status": error_message}, status=400)  # Return an error response

    # self.scope['query_string']['machine_id']
    # user_serializer = usermachineSerializer(machine.first())  # Get a single instance
    # data2 = user_serializer.data

    # Extract keys for digital_input, digital_output, analog_input, and analog_output
    input_output_data = IO_List.objects.filter(machine_id=machine.id).order_by('id')
    print('input_output_data', input_output_data)
    input_output_data_serializer = IO_list_serializer(input_output_data, many=True)
    print('input_output_data_serializer', input_output_data_serializer.data)
    input_output_data_serializer_data = input_output_data_serializer.data


    digital_input_keys = []
    digital_output_keys = []
    analog_input_keys = []
    analog_output_keys = []
    for i in range(len(input_output_data)):
        if input_output_data_serializer_data[i]['IO_type'] == "digital_input":
            digital_input_keys.append(input_output_data_serializer_data[i]['IO_name'])

        if input_output_data_serializer_data[i]['IO_type'] == "digital_output":
            digital_output_keys.append(input_output_data_serializer_data[i]['IO_name'])

        if input_output_data_serializer_data[i]['IO_type'] == "analog_input":
            analog_input_keys.append(input_output_data_serializer_data[i]['IO_name'])
        if input_output_data_serializer_data[i]['IO_type'] == "analog_output":
            analog_output_keys.append(input_output_data_serializer_data[i]['IO_name'])

    # Extract values from the payload using the corresponding keys
    digital_input = [payload.get('Dosing')]
    digital_output = [payload.get('Compressor_1'),  payload.get('Pump')]
    analog_input = [payload.get('Temperature'), payload.get('Humidity')]
    analog_output = [payload.get('Flow')]

    digital_keyvalue_input_data = []

    for key, value in zip(digital_input_keys, digital_input):
        value_str = "On" if value else "Off"
        color = None
        for i in range(len(input_output_data)):
            if input_output_data_serializer_data[i]['IO_type'] == "digital_input" and \
                    input_output_data_serializer_data[i]['IO_name'] == key:
                db_color = input_output_data_serializer_data[i]['IO_color']
                color = db_color[0] if value else db_color[1]
                break  # Exit loop once the correct key is found
            else:
                pass

        digital_keyvalue_input_data.append({"name": key, "value": value_str, "color": color})
    print('digital_keyvalue_input_data', digital_keyvalue_input_data)

    digital_keyvalue_output_data = []

    for key, value in zip(digital_output_keys, digital_output):
        value_str = "On" if value else "Off"  # Convert boolean to "On" or "Off"
        color = None
        for i in range(len(input_output_data)):
            if input_output_data_serializer_data[i]['IO_type'] == "digital_output" and \
                    input_output_data_serializer_data[i]['IO_name'] == key:
                db_color = input_output_data_serializer_data[i]['IO_color']
                color = db_color[0] if value else db_color[1]
                break  # Exit loop once the correct key is found
            else:
                pass

        digital_keyvalue_output_data.append({"name": key, "value": value_str, "color": color})
    print('digital_keyvalue_output_data', digital_keyvalue_output_data)

    analog_keyvalue_input_data = []
    for key, value in zip(analog_input_keys, analog_input):
        db_unit = None
        for i in range(len(input_output_data)):
            if input_output_data_serializer_data[i]['IO_type'] == "analog_input" and \
                    input_output_data_serializer_data[i]['IO_name'] == key:
                db_unit = input_output_data_serializer_data[i]['IO_Unit']
                color = input_output_data_serializer_data[i]['IO_color'][0]
                break  # Exit loop once the correct key is found
            else:
                pass

        analog_keyvalue_input_data.append({"name": key, "value": str(value), "color": color, "unit": db_unit})
    print('analog_keyvalue_input_data', analog_keyvalue_input_data)

    analog_keyvalue_output_data = []
    for key, value in zip(analog_output_keys, analog_output):
        db_unit = None
        for i in range(len(input_output_data)):
            if input_output_data_serializer_data[i]['IO_type'] == "analog_output" and \
                    input_output_data_serializer_data[i]['IO_name'] == key:
                db_unit = input_output_data_serializer_data[i]['IO_Unit']
                color = input_output_data_serializer_data[i]['IO_color'][0]

                break  # Exit loop once the correct key is found
            else:
                pass

        analog_keyvalue_output_data.append({"name": key, "value": str(value), "color": color, "unit": db_unit})
    print('analog_keyvalue_output_data', analog_keyvalue_output_data)

    # Create dictionaries for data to be sent

    # Construct the final result dictionary
    result = {
        'machine_id': machine_id,
        'machine_name': machine.machine_name,
        'digital_input': digital_keyvalue_input_data,
        'digital_output': digital_keyvalue_output_data,
        'analog_input': analog_keyvalue_input_data,
        'analog_output': analog_keyvalue_output_data,
        'db_timestamp': payload['timestamp']
    }

    # Convert the result dictionary to a JSON string
    res = json.dumps(result)
    channel_layer = get_channel_layer()  # get default channel layer  RedisChannelLayer(hosts=[{'address': 'redis://65.2.3.42:6379'}])
    # async_to_sync(channel_layer.group_send)(user_data, {"type": "chat.message", "text": res})
    # print('channel_layer',channel_layer)
    async_to_sync(channel_layer.group_send)(machine_id, {"type": "chat.message", "text": res})






