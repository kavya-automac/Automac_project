import asyncio

# from . models import *
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.http import JsonResponse
import json
from datetime import datetime

# from Automac_app.models import all_Machine_data,Machines_List
from asgiref.sync import sync_to_async

channel_layer_KPI = get_channel_layer()

@sync_to_async
def kpi_socket(machine_id):
    print('kkk')
    from .models import Machine_KPI_Data
    from Automac_app.models import all_Machine_data, Machines_List

    kpis = []
    try:
        machinelist= Machines_List.objects.get(machine_id=machine_id)
        print('machinelist',machinelist)
    except Machines_List.DoesNotExist:
        return JsonResponse({"status": 'machine not avaiable'}, status=400)  # Return an error response


    try:
        user_data = all_Machine_data.objects.filter(machine_id__machine_id=machinelist)
        print('users_data', user_data)
    except all_Machine_data.DoesNotExist:
        error_message = "Please enter a valid machine_id."
        return JsonResponse({"status": error_message}, status=400)  # Return an error response

    today = datetime.now().date()

    for machine_data in user_data:
        if machine_data.kpi is not None:
            kpitype = machine_data.kpi.Kpi_Type
            kpiname = machine_data.kpi.kpi_name
            kpi_labels = machine_data.kpi.labels
            kpi_result = {}

            if kpitype == 'Line_Graph':
                kpidata = Machine_KPI_Data.objects.filter(
                    machine_id=machine_data,
                    kpi_id__kpi_name=kpiname,
                    kpi_id__Kpi_Type=kpitype
                ).order_by('-timestamp').first()

                if kpidata:
                    time = kpidata.timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')  # Format timestamp as ISO string
                    value = kpidata.kpi_data

                    kpi_result['x_axis'] = time
                    kpi_result['y_axis'] = value
            elif kpitype == 'cummulative':
                kpidata = Machine_KPI_Data.objects.filter(
                    machine_id=machine_data,
                    kpi_id__kpi_name=kpiname,
                    kpi_id__Kpi_Type=kpitype,
                    timestamp__date=today
                ).order_by('-timestamp').first()

                kpitype = 'text'
                if kpidata:
                    name = kpidata.kpi_id.kpi_name
                    value = kpidata.kpi_data

                    kpi_result['value'] = value
                if 'value' not in kpi_result:
                    kpi_result['value'] = ''

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
    print('result_data', result_data)


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
