import asyncio

# from . models import *
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models.functions import TruncSecond
from django.http import JsonResponse
import json
from datetime import datetime

# from Automac_app.models import all_Machine_data,Machines_List
from asgiref.sync import sync_to_async

channel_layer_KPI = get_channel_layer()

@sync_to_async
def kpi_socket(username,machine_id):
    print('kkk1')
    from .models import Machine_KPI_Data
    print('kkk2')
    from Automac_app.models import all_Machine_data, Machines_List,IO_List
    print('kkk3')
    print('kkk4')
    todays_date=datetime.now().date()

    kpis = []
    try:
        machinelist= Machines_List.objects.get(machine_id=machine_id)
        # print('machinelist',machinelist)
    except Machines_List.DoesNotExist:
        return JsonResponse({"status": 'machine not avaiable'}, status=400)  # Return an error response


    try:
        user_data = all_Machine_data.objects.filter(user_name__username=username,machine_id__machine_id=machinelist)
        # print('users_data', user_data)
    except all_Machine_data.DoesNotExist:
        error_message = "Please enter a valid machine_id."
        return JsonResponse({"status": error_message}, status=400)  # Return an error response
    except Exception as e:
        print("eeeeeeeeee",e)
    today = datetime.now().date()
    kpis = []


    for machine_data in user_data:
        # print('machine_data',machine_data)
        # print('machine_datakpiiii',machine_data.kpi )
        if machine_data.kpi is not None:
            # print('in machine_data')
            kpitype = machine_data.kpi.kpi_inventory_id.Kpi_Type
            kpiname = machine_data.kpi.kpi_name
            kpi_labels = machine_data.kpi.kpi_inventory_id.labels
            kpi_result = {}

            if kpitype == 'Line_Graph':
                print('lineee')
                # kpidata = Machine_KPI_Data.objects.filter(machine_id=machine_data, kpi_id__kpi_name=kpiname
                #                                           , kpi_id__kpi_inventory_id__Kpi_Type=kpitype,
                #                                           timestamp__date=todays_date). \
                #     annotate(rounded_timestamp=TruncSecond('timestamp',second=30)) \
                #     .distinct('rounded_timestamp')

                kpidata = Machine_KPI_Data.objects.filter(
                    machine_id=machine_data,
                    kpi_id__kpi_name=kpiname,
                    kpi_id__kpi_inventory_id__Kpi_Type=kpitype,
                    timestamp__date=todays_date
                ).order_by('-timestamp')[::12]

                # kpidata = Machine_KPI_Data.objects.filter(
                #     machine_id=machine_data,
                #     kpi_id__kpi_name=kpiname,
                #     kpi_id__kpi_inventory_id__Kpi_Type=kpitype
                # ).order_by('-timestamp').first()
                # print('kpidataaaa',kpidata)
                x_axis = []  # List to store x-axis (timestamp)
                y_axis = []
                for kpidatatype in kpidata:
                    time = kpidatatype.timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')  # Format timestamp as ISO string
                    value_list = kpidatatype.kpi_data  # Assuming kpi_data is a list
                    processed_values = []  # List to store processed values
                    # print('value_list', value_list)
                    x_axis.append(time)
                    y_axis.append(value_list[0])


                kpi_result['x_axis'] = x_axis
                kpi_result['y_axis'] = y_axis
                if not kpi_result['x_axis']:
                    kpi_result['x_axis'] = []
                if not kpi_result['y_axis']:
                    kpi_result['y_axis'] = []



                # if kpidata:
                #     print('in if ',kpidata.timestamp)
                #     time = kpidata.timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')  # Format timestamp as ISO string
                #     value = kpidata.kpi_data
                #     x_axis.append(time)
                #     y_axis.append(value[0])
                # else:
                #     print('in else')
                #
                # kpi_result['x_axis'] = x_axis
                # kpi_result['y_axis'] = y_axis
                # print('kpi_result in line',kpi_result)
            elif kpitype == 'Text_Card':
                # print('texttttt')
                kpidata = Machine_KPI_Data.objects.filter(
                    machine_id=machine_data,
                    kpi_id__kpi_name=kpiname,
                    kpi_id__kpi_inventory_id__Kpi_Type=kpitype,
                    timestamp__date=today
                ).order_by('-timestamp').first()
                # print('kpidataaaa in text',kpidata)


                kpitype = 'text'
                if kpidata:
                    name = kpidata.kpi_id.kpi_name
                    value = kpidata.kpi_data

                    kpi_result['value'] =  kpi_result['value'] = "On" if value[0] else "Off"
                if 'value' not in kpi_result:
                    kpi_result['value'] = ''

            elif kpitype == "Energy_Card":
                print('energyyy')
                input_output_data = IO_List.objects.filter(machine_id__machine_id=machinelist).order_by('id')
                # print('input_output_data', input_output_data)
                # from .serializers import IO_list_serializer

                # input_output_data_serializer = IO_list_serializer(input_output_data, many=True)
                # print('input_output_data_serializer', input_output_data_serializer)
                # input_output_data_serializer_data = input_output_data_serializer.data
                # print('iddddddddddd',input_output_data_serializer_data[0]['machine_id'])
                # print('iiii',r_s2_d['machine_id'])

                digital_input_keys = []
                digital_output_keys = []
                analog_input_keys = []
                analog_output_keys = []
                other_keys = []
                for i in range(len(input_output_data)):
                    # print('iiiiiiiiiiiii',input_output_data[i].IO_type)
                    if input_output_data[i].IO_type== "digital_input":
                        digital_input_keys.append(input_output_data[i].IO_name)
                    #
                    # if input_output_data_serializer_data[i]['IO_type'] == "digital_output":
                    #     digital_output_keys.append(input_output_data_serializer_data[i]['IO_name'])
                    #
                    # if input_output_data_serializer_data[i]['IO_type'] == "analog_input":
                    #     analog_input_keys.append(input_output_data_serializer_data[i]['IO_name'])
                    if input_output_data[i].IO_type == "analog_output":
                        analog_output_keys.append(input_output_data[i].IO_name)
                    if input_output_data[i].IO_type == "other":
                        other_keys.append(input_output_data[i].IO_name)

                # print(other_keys)
                digital_input_value = []
                digital_output_value = []
                analog_input_value = []
                analog_output_value = []
                other_value = []
                kpi_data_table_values = Machine_KPI_Data.objects.filter(machine_id=machine_data,
                                                                        kpi_id__kpi_name=kpiname, \
                                                                        kpi_id__kpi_inventory_id__Kpi_Type=kpitype,
                                                                        timestamp__date=todays_date
                                                                        ).order_by('-timestamp').first()
                # print('kpi_data_table_values', kpi_data_table_values)
                energy_card_values = kpi_data_table_values.kpi_data
                energy_card_values_null_str = [str(item) if item is not None else "null" for item in energy_card_values]

                kpi_result['keys'] = other_keys
                kpi_result['values'] = energy_card_values_null_str


            kpi_entry = {
                'card': kpitype,
                'title': kpiname,
                'labels': kpi_labels,
                'data': kpi_result,
            }

            kpis.append(kpi_entry)

    result_data = {
        'data': kpis,
    }
    result_data['machine_id']=machinelist.machine_id
    result_data['machine_name']=machinelist.machine_name
    # print('result_data', result_data)
    result_data['user_name']=username


    res = json.dumps(result_data)

    # channel_layer = get_channel_layer()
    try:
        async_to_sync(channel_layer_KPI.group_send)(str(machine_id)+'_kpi', {"type": "kpiweb", "text": res})
    except Exception as e:
        print("kpi ws error ", e)


# @sync_to_async
# def kpi_socket(machine_id):
#
#     kpis = []
#
#     try:
#         user_data = all_Machine_data.objects.filter(machine_id__machine_id=machine_id)
#         print('user_dataaa',user_data)
#     except Machines_List.DoesNotExist:
#         error_message = "Please enter a valid machine_id."
#         return JsonResponse({"status": error_message}, status=400)  # Return an error response
#
#     today = datetime.now().date()
#
#     for machine_data in user_data:
#         if machine_data.kpi is not None:
#             kpitype = machine_data.kpi.Kpi_Type
#             kpiname = machine_data.kpi.kpi_name
#             kpi_labels = machine_data.kpi.labels
#             kpi_result = {}
#
#             if kpitype == 'Line_Graph':
#                 # Retrieve the latest record for line_graph
#                 kpidata = Machine_KPI_Data.objects.filter(
#                     machine_id=machine_data,
#                     kpi_id__kpi_name=kpiname,
#                     kpi_id__Kpi_Type=kpitype
#                 ).order_by('-timestamp').first()
#
#                 kpi_result['x_axis'] = []
#                 kpi_result['y_axis'] = []
#
#                 if kpidata:
#                     time = kpidata.timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')  # Format timestamp as ISO string
#                     value = kpidata.kpi_data
#
#                     kpi_result['x_axis'] = [time]
#                     kpi_result['y_axis'] = [value]
#
#             elif kpitype == 'cummulative':
#                 # Retrieve the most recent record for today's date
#                 kpidata = Machine_KPI_Data.objects.filter(
#                     machine_id=machine_data,
#                     kpi_id__kpi_name=kpiname,
#                     kpi_id__Kpi_Type=kpitype,
#                     timestamp__date=today
#                 ).order_by('-timestamp').first()
#
#                 kpitype = 'text'
#                 if kpidata:
#                     name = kpidata.kpi_id.kpi_name
#                     value = kpidata.kpi_data
#
#                     kpi_result['value'] = value
#
#                 # If 'value' is missing, set it to an empty string
#                 if 'value' not in kpi_result:
#                     kpi_result['value'] = ''
#
#             kpi_entry = {
#                 'card': kpitype,
#                 'title': kpiname,
#                 'labels': kpi_labels,
#                 'data': kpi_result,
#             }
#
#             kpis.append(kpi_entry)
#
#     result_data = {
#         'kpi': kpis,
#     }
#     # return result
#     # channel_layer = get_channel_layer()
#     # async_to_sync(channel_layer.group_send)(
#     #     'ABD2',
#     #     {
#     #         "type": "kpi_web",
#     #         "result_data": result_data,
#     #     },
#     # )
#
#     res = json.dumps(result_data)
#     # return res
#
#     channel_layer = get_channel_layer()  # get default channel layer  RedisChannelLayer(hosts=[{'address': 'redis://65.2.3.42:6379'}])
#     await channel_layer.group_add(machine_id, self.channel_name)  # Add the consumer to a group
#     await channel_layer.group_send(machine_id, {"type": "kpi.web", "text": res})
#     # async_to_sync(channel_layer.group_send)(user_data, {"type": "chat.message", "text": res})
#     # print('channel_layer',channel_layer)
#     # async_to_sync(channel_layer.group_send)(machine_id, {"type": "kpi.web", "text": res})
# =================================================================================
