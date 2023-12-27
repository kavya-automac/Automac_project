import datetime

from django.db.models import Sum
from django.db.models.functions import Extract
from django.http import JsonResponse
from rest_framework.response import Response

from .serializers import *

from Automac_machines_app.serializers import machineSerializer,machineSerializer_two
from Automac_machines_app.models import MachineDetails


def history_fun(machine_id,date):
    machine_value_data = MachineDetails.objects.filter(machine_id=machine_id, timestamp__date=date).\
    values('timestamp','machine_id','machine_location','digital_input','digital_output','analog_input','analog_output','other').distinct('timestamp').order_by('-timestamp')[:50]
    # machine_value_data = MachineDetails.objects.filter(machine_id=machine_id, timestamp__date=date).order_by('-timestamp')[:50]

    # details = MachineDetails.objects.filter(machine_id=machine_id, timestamp__date=date).order_by('-timestamp')[:50]
    # print('details',details)

    # details = MachineDetails.objects.filter(machine_id=machine_id, timestamp__range=[start_datetime, end_datetime])
    # print('details',len(machine_value_data))
    serializer = machineSerializer(machine_value_data, many=True)

    r_s_d = serializer.data
    # print('r_s_d',r_s_d)
    digital_input_value = []
    digital_output_value = []
    analog_input_value = []
    analog_output_value = []
    other_value=[]

    for d in range(0, len(r_s_d)):
        digital_input_value.append(r_s_d[d]['digital_input'])
        digital_output_value.append(r_s_d[d]['digital_output'])
        analog_input_value.append(r_s_d[d]['analog_input'])
        analog_output_value.append(r_s_d[d]['analog_output'])
        other_value.append(r_s_d[d]['other'])

    # print('digital_input_value',digital_input_value)

    from .views import null_to_str
    digital_input_value = null_to_str(digital_input_value)
    digital_output_value = null_to_str(digital_output_value)
    analog_input_value = null_to_str(analog_input_value)
    analog_output_value = null_to_str(analog_output_value)
    other_value = null_to_str(other_value)
    for inner_list in digital_input_value:
        for i in range(len(inner_list)):
            if inner_list[i] == 'True':
                inner_list[i] = 'On'
            elif inner_list[i] == 'False':
                inner_list[i] = 'Off'
    # print('siv',digital_input_value)


    # Convert 'True' to 'On' and 'False' to 'Off' in the list of lists for digital_output_value
    for inner_list in digital_output_value:
        for i in range(len(inner_list)):
            if inner_list[i] == 'True':
                inner_list[i] = 'On'
            elif inner_list[i] == 'False':
                inner_list[i] = 'Off'
    # print(digital_input_value)
    # print(digital_output_value)
    # print(analog_input_value)
    # print(analog_output_value)
    try:
        machine = Machines_List.objects.get(machine_id=machine_id)
    except Machines_List.DoesNotExist:
        error_message = "Please enter a valid machine_id."
        return JsonResponse({"status": error_message}, status=400)  # Return an error response
    serializer_2 = usermachineSerializer(machine)
    r_s2_d = serializer_2.data


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
    other_keys=[]
    for i in range(len(input_output_data)):
        if input_output_data_serializer_data[i]['IO_type'] == "digital_input":
            digital_input_keys.append(input_output_data_serializer_data[i]['IO_name'])

        if input_output_data_serializer_data[i]['IO_type'] == "digital_output":
            digital_output_keys.append(input_output_data_serializer_data[i]['IO_name'])

        if input_output_data_serializer_data[i]['IO_type'] == "analog_input":
            analog_input_keys.append(input_output_data_serializer_data[i]['IO_name'])
        if input_output_data_serializer_data[i]['IO_type'] == "analog_output":
            analog_output_keys.append(input_output_data_serializer_data[i]['IO_name'])
        if input_output_data_serializer_data[i]['IO_type'] == "other":
            other_keys.append(input_output_data_serializer_data[i]['IO_name'])








    # d_i_k = r_s2_d['digital_input']
    # d_o_k = r_s2_d['digital_output']
    # a_i_k = r_s2_d['analog_input']
    # a_o_k = r_s2_d['analog_output']
    # print('dkkkk',d_i_k)
    # print('dok',d_o_k)
    # print('aik',a_i_k)
    # print('aok',a_o_k)
    result_data=[]



    if  r_s_d:
        # print('iffff',not r_s_d)
        for i in range(len(r_s_d)):
            # d_i_res = [{'name': key, 'value': value} for key, value in zip(digital_input_keys, digital_input_value[i])]
            # # print('d_i_res',d_i_res)
            #
            # d_o_res = [{'name': key, 'value': value} for key, value in zip(digital_output_keys, digital_output_value[i])]
            # a_i_res = [{'name': key, 'value': value} for key, value in zip(analog_input_keys, analog_input_value[i])]
            # a_o_res = [{'name': key, 'value': value} for key, value in zip(analog_output_keys, analog_output_value[i])]
            d_i_res = []

            for key, value in zip(digital_input_keys, digital_input_value[i]):
                # Convert boolean to "On" or "Off"
                color = None
                for k in range(len(input_output_data)):
                    if input_output_data_serializer_data[k]['IO_type'] == "digital_input" and \
                            input_output_data_serializer_data[k]['IO_name'] == key:
                        db_unit = input_output_data_serializer_data[k]['IO_Unit']

                        db_color = input_output_data_serializer_data[k]['IO_color']
                        if value == "On":
                            color = db_color[0]
                        if value == "Off":
                            color = db_color[1]
                        # color = db_color[0] if value else db_color[1]
                        break  # Exit loop once the correct key is found
                    else:
                        pass
                d_i_res.append({'name': key, 'value': value, 'color': color,'unit':db_unit})
                # print('inputttt', d_i_res)

            d_o_res = []

            for key, value in zip(digital_output_keys, digital_output_value[i]):
                # Convert boolean to "On" or "Off"
                color = None
                for k in range(len(input_output_data)):
                    if input_output_data_serializer_data[k]['IO_type'] == "digital_output" and \
                            input_output_data_serializer_data[k]['IO_name'] == key:
                        db_unit = input_output_data_serializer_data[k]['IO_Unit']

                        db_color = input_output_data_serializer_data[k]['IO_color']
                        if value == "On":
                            color = db_color[0]
                        if value == "Off":
                            color = db_color[1]
                        # color = db_color[0] if value else db_color[1]
                        break  # Exit loop once the correct key is found
                    else:
                        pass
                d_o_res.append({'name': key, 'value': value, 'color': color,'unit':db_unit})
                # print('d outputttt', d_o_res)

            a_i_res = []

            for key, value in zip(analog_input_keys, analog_input_value[i]):
                # Convert boolean to "On" or "Off"
                db_unit = None
                color = None
                for k in range(len(input_output_data)):
                    if input_output_data_serializer_data[k]['IO_type'] == "analog_input" and \
                            input_output_data_serializer_data[k]['IO_name'] == key:
                        db_unit = input_output_data_serializer_data[k]['IO_Unit']
                        color = input_output_data_serializer_data[k]['IO_color'][0]

                        break  # Exit loop once the correct key is found
                    else:
                        pass
                a_i_res.append({'name': key, 'value': value,'color':color, 'unit': db_unit})
                # print('aa inputputttt', a_i_res)

            a_o_res = []

            for key, value in zip(analog_output_keys, analog_output_value[i]):
                # Convert boolean to "On" or "Off"
                db_unit = None
                color = None
                for k in range(len(input_output_data)):
                    if input_output_data_serializer_data[k]['IO_type'] == "analog_output" and \
                            input_output_data_serializer_data[k]['IO_name'] == key:
                        db_unit = input_output_data_serializer_data[k]['IO_Unit']
                        color = input_output_data_serializer_data[k]['IO_color'][0]

                        break  # Exit loop once the correct key is found
                    else:
                        pass
                a_o_res.append({'name': key, 'value': value,'color':color, 'unit': db_unit})
                # print('aaa outputttt', a_o_res)

            other_res = []

            for key, value in zip(other_keys, other_value[i]):
                # Convert boolean to "On" or "Off"
                db_unit = None
                color = None
                for k in range(len(input_output_data)):
                    if input_output_data_serializer_data[k]['IO_type'] == "other" and \
                            input_output_data_serializer_data[k]['IO_name'] == key:
                        db_unit = input_output_data_serializer_data[k]['IO_Unit']
                        color = input_output_data_serializer_data[k]['IO_color'][0]

                        break  # Exit loop once the correct key is found
                    else:
                        pass
                other_res.append({'name': key, 'value': value, 'color': color, 'unit': db_unit})
                # print('aaa outputttt', a_o_res)

            data_entries = d_i_res + d_o_res + a_i_res + a_o_res+other_res
            # print('dtaaaaaaaaaaaaa',data_entries)


            entry = {

                        "data": data_entries,
            "timestamp": serializer.data[i]['timestamp']

                        }


            # entry.update({"timestamp":r_s_d[i]['timestamp']})
            # print('lllllllll',entry)

            result_data.append(entry)
        # print('resulttttttttttttttttttttt',result_data)
        resultant_data = {
            "machine_details":{
            "machine_id": r_s2_d['machine_id'],
            "machine_name": r_s2_d['machine_name']},
            "Trail_Details": result_data
        }
        # print("jsonresponse result",result_data)


        return JsonResponse(resultant_data)
    else:
        resultant_data = {
            "machine_details": {
                "machine_id": r_s2_d['machine_id'],
                "machine_name": r_s2_d['machine_name']},
            "Trail_Details": result_data

        }
        return JsonResponse(resultant_data)




