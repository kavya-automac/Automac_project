import datetime

from django.http import JsonResponse
from rest_framework.response import Response

from .serializers import *

from Automac_machines_app.serializers import machineSerializer,machineSerializer_two
from Automac_machines_app.models import MachineDetails


def history_fun(machine_id,date):
    details = MachineDetails.objects.filter(machine_id=machine_id, timestamp__date=date)[:50]
    # print('details',details)

    # details = MachineDetails.objects.filter(machine_id=machine_id, timestamp__range=[start_datetime, end_datetime])
    print('details',len(details))
    serializer = machineSerializer(details, many=True)

    r_s_d = serializer.data
    # print('r_s_d',r_s_d)
    d_i_v = []
    d_o_v = []
    a_i_v = []
    a_o_v = []

    for d in range(0, len(r_s_d)):
        d_i_v.append(r_s_d[d]['digital_input'])
        d_o_v.append(r_s_d[d]['digital_output'])
        a_i_v.append(r_s_d[d]['analog_input'])
        a_o_v.append(r_s_d[d]['analog_output'])
    # print('d_i_v',d_i_v)

    from .views import null_to_str
    d_i_v = null_to_str(d_i_v)
    d_o_v = null_to_str(d_o_v)
    a_i_v = null_to_str(a_i_v)
    a_o_v = null_to_str(a_o_v)
    for inner_list in d_i_v:
        for i in range(len(inner_list)):
            if inner_list[i] == 'True':
                inner_list[i] = 'On'
            elif inner_list[i] == 'False':
                inner_list[i] = 'Off'
    # print('siv',d_i_v)


    # Convert 'True' to 'On' and 'False' to 'Off' in the list of lists for d_o_v
    for inner_list in d_o_v:
        for i in range(len(inner_list)):
            if inner_list[i] == 'True':
                inner_list[i] = 'On'
            elif inner_list[i] == 'False':
                inner_list[i] = 'Off'
    print(d_i_v)
    print(d_o_v)
    print(a_i_v)
    print(a_o_v)

    keys = Machines_List.objects.get(machine_id=machine_id)
    serializer_2 = usermachineSerializer(keys)
    r_s2_d = serializer_2.data
    # print('hhhhhhhhhhhhhhhh',r_s2_d)
    # print('r_s2_d', r_s2_d)

    d_i_k = r_s2_d['digital_input']
    d_o_k = r_s2_d['digital_output']
    a_i_k = r_s2_d['analog_input']
    a_o_k = r_s2_d['analog_output']

    result_data=[]

    if  r_s_d:
        # print('iffff',not r_s_d)
        for i in range(len(r_s_d)):
            d_i_res = [{'name': key, 'value': value} for key, value in zip(d_i_k, d_i_v[i])]
            print('d_i_res',d_i_res)
            d_o_res = [{'name': key, 'value': value} for key, value in zip(d_o_k, d_o_v[i])]
            a_i_res = [{'name': key, 'value': value} for key, value in zip(a_i_k, a_i_v[i])]
            a_o_res = [{'name': key, 'value': value} for key, value in zip(a_o_k, a_o_v[i])]


            data_entries = d_i_res + d_o_res + a_i_res + a_o_res
            # print('dtaaaaaaaaaaaaa',data_entries)

            entry = {

                            "data": data_entries
                        }


            entry.update({"timestamp":r_s_d[i]['timestamp']})
            # print('lllllllll',entry)

            result_data.append(entry)
    resultant_data = {
        "machine_details":{
        "machine_id": r_s2_d['machine_id'],
        "machine_name": r_s2_d['machine_name']},
        "Trail_Details": result_data
    }
    # print("rewwwwwwwwwsw",type(resultant_data))


    return JsonResponse(resultant_data)
