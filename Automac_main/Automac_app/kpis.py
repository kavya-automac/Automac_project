import datetime

from Automac_machines_app.serializers import machineSerializer,analog_ip_op_Serializer,\
    machineSerializer_two,analog_ip_op_Serializer,kpi_data_Serializer,kpi_cummulative_serilaizer
from Automac_machines_app.models import MachineDetails,Machine_KPI_Data
from django.http import JsonResponse

from .serializers import *
from rest_framework.decorators import action

from rest_framework.response import Response

from .serializers import *

# from . import calculations

from django.http import JsonResponse
from django.http import JsonResponse
from datetime import datetime, timedelta


from django.http import JsonResponse
from datetime import datetime, timedelta
from django.http import JsonResponse

from datetime import datetime
from django.http import JsonResponse

def get_kpis_data(user, machine):
    kpis = []

    try:
        user_data = all_Machine_data.objects.filter(user_name=user, machine_id=machine)
        print('userrrrrrrr',user_data)
    except Machines_List.DoesNotExist:
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
                # Retrieve the latest 10 records for line_graph
                kpidata = Machine_KPI_Data.objects.filter(
                    machine_id=machine_data,
                    kpi_id__kpi_name=kpiname,
                    kpi_id__Kpi_Type=kpitype
                ).order_by('-timestamp')[:10]  # Order by timestamp in descending order
                kpiserializer = kpi_data_Serializer(kpidata, many=True)
                kpiserializer_data = kpiserializer.data
                x_axis = []  # List to store x-axis (timestamp)
                y_axis = []  # List to store y-axis (values)
                for kpidatatype in kpidata:
                    time = kpidatatype.timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')  # Format timestamp as ISO string
                    value = kpidatatype.kpi_data

                    x_axis.append(time)
                    y_axis.append(value)

                kpi_result['x_axis'] = x_axis
                kpi_result['y_axis'] = y_axis

                # If x_axis and y_axis are empty, set them to empty lists
                if not kpi_result['x_axis']:
                    kpi_result['x_axis'] = []
                if not kpi_result['y_axis']:
                    kpi_result['y_axis'] = []

            elif kpitype == 'cummulative':
                # Retrieve the most recent record for today's date
                kpidata = Machine_KPI_Data.objects.filter(
                    machine_id=machine_data,
                    kpi_id__kpi_name=kpiname,
                    kpi_id__Kpi_Type=kpitype,
                    timestamp__date=today
                ).order_by('-timestamp').first()
                print('---------------------------', kpidata)

                kpitype = 'text'
                if kpidata:
                    name = kpidata.kpi_id.kpi_name
                    value = kpidata.kpi_data
                    print('value', value)

                    kpi_result['value'] = value

                # If 'value' is missing, set it to an empty string
                if 'value' not in kpi_result:
                    kpi_result['value'] = ''

            kpi_entry = {
                'card': kpitype,
                'title': kpiname,
                'labels': kpi_labels,
                'data': kpi_result,
            }

            kpis.append(kpi_entry)

    result = {
        'kpi': kpis,
    }
    return result





# def get_kpis_data(user, machine):
#     kpis = []
#
#     try:
#         user_data = all_Machine_data.objects.filter(user_name=user, machine_id=machine)
#     except Machines_List.DoesNotExist:
#         error_message = "Please enter a valid machine_id."
#         return JsonResponse({"status": error_message}, status=400)  # Return an error response
#
#     today = datetime.now().date()
#
#     for machine_data in user_data:
#         if machine_data.kpi is not None:  # Check if kpi is not None
#             kpitype = machine_data.kpi.Kpi_Type
#             kpiname = machine_data.kpi.kpi_name
#             kpi_labels = machine_data.kpi.labels
#             kpi_result = {}
#
#             if kpitype == 'Line_Graph':
#                 # Retrieve the latest 10 records for line_graph
#                 kpidata = Machine_KPI_Data.objects.filter(
#                     machine_id=machine_data,
#                     kpi_id__kpi_name=kpiname,
#                     kpi_id__Kpi_Type=kpitype
#                 ).order_by('-timestamp')[:10]  # Order by timestamp in descending order
#                 kpiserializer=kpi_data_Serializer(kpidata,many=True)
#                 kpiserializer_data=kpiserializer.data
#                 x_axis = []  # List to store x-axis (timestamp)
#                 y_axis = []  # List to store y-axis (values)
#                 for kpidatatype in kpidata:
#                     time = kpidatatype.timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')  # Format timestamp as ISO string
#                     value = kpidatatype.kpi_data
#
#                     x_axis.append(time)
#                     y_axis.append(value)
#
#                 kpi_result['x_axis'] = x_axis
#                 kpi_result['y_axis'] = y_axis
#
#
#
#             elif kpitype == 'cummulative':
#
#                 # Retrieve the most recent record for today's date
#                 kpidata = Machine_KPI_Data.objects.filter(
#                     machine_id=machine_data,
#                     kpi_id__kpi_name=kpiname,
#                     kpi_id__Kpi_Type=kpitype,
#                     timestamp__date=today
#                 ).order_by('-timestamp').first()
#                 print('---------------------------',kpidata)
#                 # kpiserializer = kpi_data_Serializer(kpidata, many=True)
#                 # kpiserializer_data = kpiserializer.data
#
#                 kpitype = 'text'
#                 if kpidata:
#
#                     name = kpidata.kpi_id.kpi_name
#
#
#                     value = kpidata.kpi_data
#                     print('value',value)
#
#
#                     kpi_result['value'] = value
#
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
#     result = {
#         'kpi': kpis,
#     }
#     return result



#
# def get_kpis_data(user, machine):
#     cards = []
#     line_graphs = []
#
#     try:
#         user_data = all_Machine_data.objects.filter(user_name=user, machine_id=machine)
#     except Machines_List.DoesNotExist:
#         error_message = "Please enter a valid machine_id."
#         return JsonResponse({"status": error_message}, status=400)  # Return an error response
#
#     today = datetime.now().date()
#
#     for machine_data in user_data:
#         if machine_data.kpi is not None:  # Check if kpi is not None
#             kpitype = machine_data.kpi.Kpi_Type
#             kpiname = machine_data.kpi.kpi_name
#
#             if kpitype == 'Line_Graph':
#                 # Retrieve the latest 10 records for line_graph
#                 kpidata = Machine_KPI_Data.objects.filter(
#                     machine_id=machine_data,
#                     kpi_id__kpi_name=kpiname,
#                     kpi_id__Kpi_Type=kpitype
#                 ).order_by('-timestamp')[:10]  # Order by timestamp in descending order
#
#                 x_axis = []  # List to store x-axis (timestamp)
#                 y_axis = []  # List to store y-axis (values)
#                 for kpidatatype in kpidata:
#                     time = kpidatatype.timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')  # Format timestamp as ISO string
#                     value = kpidatatype.kpi_data
#
#                     x_axis.append(time)
#                     y_axis.append(value)
#
#                 line_graph_entry = {
#                     'card_type': 'line_graph',
#                     'title': kpiname,
#                     'x_axis': x_axis,
#                     'y_axis': y_axis,
#                 }
#
#                 line_graphs.append(line_graph_entry)
#
#             elif kpitype == 'cummulative':  # Correct the spelling to 'cumulative'
#                 # Retrieve the most recent record for today's date
#                 kpidata = Machine_KPI_Data.objects.filter(
#                     machine_id=machine_data,
#                     kpi_id__kpi_name=kpiname,
#                     kpi_id__Kpi_Type=kpitype,
#                     timestamp__date=today
#                 ).order_by('-timestamp').first()
#
#                 if kpidata:
#                     name = kpidata.kpi_id.kpi_name
#                     unit = kpidata.kpi_id.kpi_unit
#                     value = kpidata.kpi_data
#
#                     kpi_entry = {
#                         'type': 'text',
#                         'title': name,
#                         'value': value,
#                         'units': unit,
#                     }
#
#                     cards.append(kpi_entry)
#
#     result = {
#         'line_graphs': line_graphs,
#         'cards': cards,
#     }
#     return result

#
# def get_kpis_data(user, machine):
#     cards = []
#     line_graphs = []
#
#     try:
#         user_data = all_Machine_data.objects.filter(user_name=user, machine_id=machine)
#     except Machines_List.DoesNotExist:
#         error_message = "Please enter a valid machine_id."
#         return JsonResponse({"status": error_message}, status=400)  # Return an error response
#
#     for machine_data in user_data:
#         if machine_data.kpi is not None:  # Check if kpi is not None
#             kpitype = machine_data.kpi.Kpi_Type
#             kpiname = machine_data.kpi.kpi_name
#
#             if kpitype == 'Line_Graph':
#                 # Retrieve the latest 10 records for line_graph
#                 kpidata = Machine_KPI_Data.objects.filter(
#                     machine_id=machine_data,
#                     kpi_id__kpi_name=kpiname,
#                     kpi_id__Kpi_Type=kpitype
#                 ).order_by('-timestamp')[:10]  # Order by timestamp in descending order
#
#                 x_axis = []  # List to store x-axis (timestamp)
#                 y_axis = []  # List to store y-axis (values)
#                 for kpidatatype in kpidata:
#                     time = kpidatatype.timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')  # Format timestamp as ISO string
#                     value = kpidatatype.kpi_data
#
#                     x_axis.append(time)
#                     y_axis.append(value)
#
#                 line_graph_entry = {
#                     'card_type': 'line_graph',
#                     'title': kpiname,
#                     'x_axis': x_axis,
#                     'y_axis': y_axis,
#                 }
#
#                 line_graphs.append(line_graph_entry)
#
#             elif kpitype == 'cummulative':  # Correct the spelling to 'cumulative'
#                 # Retrieve all records for cumulative
#                 kpidata = Machine_KPI_Data.objects.filter(
#                     machine_id=machine_data,
#                     kpi_id__kpi_name=kpiname,
#                     kpi_id__Kpi_Type=kpitype
#                 )
#
#                 for kpidatatype in kpidata:
#                     name = kpidatatype.kpi_id.kpi_name
#                     unit = kpidatatype.kpi_id.kpi_unit
#                     value = kpidatatype.kpi_data
#
#                     kpi_entry = {
#                         'type': 'cummulative',  # Add the 'type' field
#                         'title': name,
#                         'value': value,
#                         'units': unit,  # Add the 'units' field
#                     }
#
#                     cards.append(kpi_entry)
#
#     result = {
#         'line_graphs': line_graphs,
#         'cards': cards,
#     }
#     return result




# def get_kpis_data(user,machine):
#     res = []
#     cumulative_data = []
#     line_graph_data = []
#
#     try:
#         user_data = all_Machine_data.objects.filter(user_name=user,machine_id=machine)
#     except Machines_List.DoesNotExist:
#         error_message = "Please enter a valid machine_id."
#         return JsonResponse({"status": error_message}, status=400)  # Return an error response
#     print('user_data',user_data)
#     print('user_data',len(user_data))
#     for machine_data in user_data:
#         if machine_data.kpi is not None:  # Check if kpi is not None
#             kpitype = machine_data.kpi.Kpi_Type
#             kpiname = machine_data.kpi.kpi_name
#
#             if kpitype == 'Line_Graph':
#                 # Retrieve the latest 10 records for line_graph
#                 kpidata = Machine_KPI_Data.objects.filter(
#                     machine_id=machine_data,
#                     kpi_id__kpi_name=kpiname,
#                     kpi_id__Kpi_Type=kpitype
#                 ).order_by('-timestamp')[:10]  # Order by timestamp in descending order
#
#                 data_list = []  # List to store the data for this kpiName
#                 for kpidatatype in kpidata:
#                     time = kpidatatype.timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')  # Format timestamp as ISO string
#                     value = kpidatatype.kpi_data
#
#                     data_entry = {
#                         'time': time,
#                         'value': value,
#                     }
#
#                     data_list.append(data_entry)
#
#                 line_graph_entry = {
#                     'kpiName': kpiname,
#                     'data': data_list,
#                 }
#
#                 line_graph_data.append(line_graph_entry)
#
#             elif kpitype == 'cummulative':
#                 # Retrieve all records for cumulative
#                 kpidata = Machine_KPI_Data.objects.filter(
#                     machine_id=machine_data,
#                     kpi_id__kpi_name=kpiname,
#                     kpi_id__Kpi_Type=kpitype
#                 )
#
#                 for kpidatatype in kpidata:
#                     name = kpidatatype.kpi_id.kpi_name
#                     unit = kpidatatype.kpi_id.kpi_unit
#                     value = kpidatatype.kpi_data
#
#                     kpi_entry = {
#                         'title': name,
#                         'unit': unit,
#                         'value': value,
#                     }
#
#                     cumulative_data.append(kpi_entry)
#
#     resulttt = {
#         'line_graph': line_graph_data,
#         'cumulative': cumulative_data,
#     }
#     return resulttt
#