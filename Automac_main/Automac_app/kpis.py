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





from datetime import datetime, timedelta

from datetime import datetime
from django.http import JsonResponse

def get_kpis_data(user, machine):
    kpis = []

    try:
        user_data = all_Machine_data.objects.filter(user_name__username=user, machine_id=machine)
        print('userrrrrrrr',user_data)
    except all_Machine_data.DoesNotExist:
        error_message = "Please enter a valid machine_id."
        return JsonResponse({"status": error_message}, status=400)  # Return an error response



    today = datetime.now().date()

    for machine_data in user_data:
        if machine_data.kpi is not None:
            kpitype = machine_data.kpi.kpi_inventory_id.Kpi_Type
            kpiname = machine_data.kpi.kpi_name
            kpi_labels = machine_data.kpi.kpi_inventory_id.labels
            kpi_result = {}


            input_output_data = IO_List.objects.filter(machine_id=machine.id).order_by('id')
            # print('input_output_data', input_output_data)
            input_output_data_serializer = IO_list_serializer(input_output_data, many=True)
            # print('input_output_data_serializer', input_output_data_serializer)
            input_output_data_serializer_data = input_output_data_serializer.data
            # print('iddddddddddd',input_output_data_serializer_data[0]['machine_id'])
            # print('iiii',r_s2_d['machine_id'])



            if kpitype == 'Line_Graph':

                # Retrieve the latest 10 records for line_graph
                kpidata = Machine_KPI_Data.objects.filter(
                    machine_id=machine_data,
                    kpi_id__kpi_name=kpiname,
                    kpi_id__kpi_inventory_id__Kpi_Type=kpitype
                ).order_by('-timestamp')[:10]  # Order by timestamp in descending order
                kpiserializer = kpi_data_Serializer(kpidata, many=True)
                kpiserializer_data = kpiserializer.data
                x_axis = []  # List to store x-axis (timestamp)
                y_axis = []  # List to store y-axis (values)
                for kpidatatype in kpidata:
                    time = kpidatatype.timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')  # Format timestamp as ISO string
                    value_list = kpidatatype.kpi_data  # Assuming kpi_data is a list
                    processed_values = []  # List to store processed values
                    print('value_list',value_list)
                    for i in range(len(input_output_data)):
                        # print('.........')
                        if input_output_data_serializer_data[i]['IO_type'] == "digital_input" and \
                            input_output_data_serializer_data[i]['IO_name'] == kpiname:
                            kpi_labels['y_label']=input_output_data_serializer_data[i]['IO_Unit']





                        if input_output_data_serializer_data[i]['IO_type'] == "digital_output" and \
                                input_output_data_serializer_data[i]['IO_name'] == kpiname:
                            kpi_labels['y_label']=input_output_data_serializer_data[i]['IO_Unit']




                        if input_output_data_serializer_data[i]['IO_type'] == "analog_input" and\
                                input_output_data_serializer_data[i]['IO_name'] == kpiname:
                            kpi_labels['y_label']=input_output_data_serializer_data[i]['IO_Unit']


                        if input_output_data_serializer_data[i]['IO_type'] == "analog_output" and \
                                input_output_data_serializer_data[i]['IO_name'] == kpiname:
                            kpi_labels['y_label']=input_output_data_serializer_data[i]['IO_Unit']


                        if input_output_data_serializer_data[i]['IO_type'] == "other" and \
                                input_output_data_serializer_data[i]['IO_name'] == kpiname:
                            kpi_labels['y_label']=input_output_data_serializer_data[i]['IO_Unit']


                    x_axis.append(time)
                    y_axis.append(value_list[0])

                    # value = kpidatatype.kpi_data
                    # print('valueeeeeee',value)
                    #
                    # x_axis.append(time)
                    # y_axis.append(value)

                kpi_result['x_axis'] = x_axis
                kpi_result['y_axis'] = y_axis

                # If x_axis and y_axis are empty, set them to empty lists
                if not kpi_result['x_axis']:
                    kpi_result['x_axis'] = []
                if not kpi_result['y_axis']:
                    kpi_result['y_axis'] = []

            elif kpitype == 'Text_Card':
                # Retrieve the most recent record for today's date
                kpidata = Machine_KPI_Data.objects.filter(
                    machine_id=machine_data,
                    kpi_id__kpi_name=kpiname,
                    kpi_id__kpi_inventory_id__Kpi_Type=kpitype,
                    timestamp__date=today
                ).order_by('-timestamp').first()
                # print('---------------------------', kpidata)

                kpitype = 'text'
                if kpidata:
                    name = kpidata.kpi_id.kpi_name
                    value = kpidata.kpi_data
                    print('value', value)

                    kpi_result['value'] = "On" if value[0] else "Off"
                    # kpi_result['value'] = value[0]

                # If 'value' is missing, set it to an empty string
                if 'value' not in kpi_result:
                    kpi_result['value'] = ''
            elif kpitype =="Energy_Card":
                input_output_data = IO_List.objects.filter(machine_id=machine.id).order_by('id')
                # print('input_output_data', input_output_data)
                input_output_data_serializer = IO_list_serializer(input_output_data, many=True)
                # print('input_output_data_serializer', input_output_data_serializer)
                input_output_data_serializer_data = input_output_data_serializer.data
                # print('iddddddddddd',input_output_data_serializer_data[0]['machine_id'])
                # print('iiii',r_s2_d['machine_id'])

                digital_input_keys = []
                digital_output_keys = []
                analog_input_keys = []
                analog_output_keys = []
                other_keys = []
                for i in range(len(input_output_data)):
                    # if input_output_data_serializer_data[i]['IO_type'] == "digital_input":
                    #     digital_input_keys.append(input_output_data_serializer_data[i]['IO_name'])
                    #
                    # if input_output_data_serializer_data[i]['IO_type'] == "digital_output":
                    #     digital_output_keys.append(input_output_data_serializer_data[i]['IO_name'])
                    #
                    # if input_output_data_serializer_data[i]['IO_type'] == "analog_input":
                    #     analog_input_keys.append(input_output_data_serializer_data[i]['IO_name'])
                    # if input_output_data_serializer_data[i]['IO_type'] == "analog_output":
                    #     analog_output_keys.append(input_output_data_serializer_data[i]['IO_name'])
                    if input_output_data_serializer_data[i]['IO_type'] == "other":
                        other_keys.append(input_output_data_serializer_data[i]['IO_name'])

                print(other_keys)
                digital_input_value = []
                digital_output_value = []
                analog_input_value = []
                analog_output_value = []
                other_value = []
                kpi_data_table_values=Machine_KPI_Data.objects.filter(machine_id=machine_data,kpi_id__kpi_name=kpiname, \
                        kpi_id__kpi_inventory_id__Kpi_Type = kpitype
                ).order_by('-timestamp')[:10].first()
                print('kpi_data_table_values',kpi_data_table_values)
                energy_card_values=kpi_data_table_values.kpi_data
                print('energy_card_values',energy_card_values)
                #......none to "null"
                energy_card_values_null_str = [str(item) if item is not None else "None" for item in energy_card_values]

                kpi_result['keys'] = other_keys
                kpi_result['values'] = energy_card_values_null_str









            kpi_entry = {
                'card': kpitype,
                'title': kpiname,
                'labels': kpi_labels,
                'data': kpi_result,
            }

            kpis.append(kpi_entry)

    result = {
        'data': kpis,
    }

    return result


