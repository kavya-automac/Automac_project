from django.http import JsonResponse

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
    print('hhhhhhhhhhhhhhhh',r_s2_d)
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
            print('dtaaaaaaaaaaaaa',data_entries)


            entry = {
                "db_timestamp": r_s_d[i]['db_timestamp'],
                "timestamp": r_s_d[i]['timestamp'],
                "machine_id": r_s_d[i]['machine_id'],
                "machine_location": r_s_d[i]['machine_location'],
                "data": data_entries
            }
            result_data.append(entry)
    else:
        # print('elseeee',not r_s_d)
        entry = {
            # "db_timestamp": date,
            # "timestamp": r_s_d[i]['timestamp'],
            "machine_id": r_s2_d['machine_id'],
            "machine_location": r_s2_d['machine_location'],
            "data": []
        }
        result_data.append(entry)



    return JsonResponse({"History": result_data})






#
# def history_fun(machine_id,date):
#
#     details = MachineDetails.objects.filter(machine_id=machine_id, timestamp__date=date)[:50]
#     print('details',details)
#
#     # details = MachineDetails.objects.filter(machine_id=machine_id, timestamp__range=[start_datetime, end_datetime])
#     print('details',len(details))
#     serializer = machineSerializer(details, many=True)
#
#     r_s_d = serializer.data
#     print('r_s_d',r_s_d)
#
#     # print('serializer.data', r_s_d[0]['digital_input'])
#     d_i_v = []
#     d_o_v = []
#     a_i_v = []
#     a_o_v = []
#
#     for d in range(0, len(r_s_d)):
#         d_i_v.append(r_s_d[d]['digital_input'])
#         d_o_v.append(r_s_d[d]['digital_output'])
#         a_i_v.append(r_s_d[d]['analog_input'])
#         a_o_v.append(r_s_d[d]['analog_output'])
#     print('d_i_v',d_i_v)
#     from .views import null_to_str
#     d_i_v = null_to_str(d_i_v)
#     d_o_v = null_to_str(d_o_v)
#     a_i_v = null_to_str(a_i_v)
#     a_o_v = null_to_str(a_o_v)
#     # print('siv',d_i_v)
#     for inner_list in d_i_v:
#         for i in range(len(inner_list)):
#             if inner_list[i] == 'True':
#                 inner_list[i] = 'On'
#             elif inner_list[i] == 'False':
#                 inner_list[i] = 'Off'
#     # print('siv',d_i_v)
#
#
#     # Convert 'True' to 'On' and 'False' to 'Off' in the list of lists for d_o_v
#     for inner_list in d_o_v:
#         for i in range(len(inner_list)):
#             if inner_list[i] == 'True':
#                 inner_list[i] = 'On'
#             elif inner_list[i] == 'False':
#                 inner_list[i] = 'Off'
#
#
#
#     # print('d_i_v', d_i_v)
#     # print('d_o_v', d_o_v)
#     # print('a_i_v', a_i_v)
#     # print('a_o_v', a_o_v)
#     keys = Machines_List.objects.all()
#     serializer_2 = usermachineSerializer(keys, many=True)
#     r_s2_d = serializer_2.data
#     # print('r_s2_d', r_s2_d)
#
#     d_i_k = r_s2_d[0]['digital_input']
#     d_o_k = r_s2_d[0]['digital_output']
#     a_i_k = r_s2_d[0]['analog_input']
#     a_o_k = r_s2_d[0]['analog_output']
#
#     # print('d_i_k', d_i_k)
#     # print('d_o_k', d_o_k)
#     # print('a_i_k', a_i_k)
#     # print('a_o_k', a_o_k)
#
#
#
#     # d_i_res = {}
#     # d_o_res = {}
#     # a_i_res = {}
#     # a_o_res = {}
#     # for key, value in zip(d_i_k, d_i_v[i]):
#     #     d_i_res.append({"name": key, "value": value})
#     #
#     # print('d_i_res', d_i_res)
#     #
#     # for key, value in zip(d_o_k, d_o_v[i]):
#     #     d_o_res.append({"name": key, "value": value})
#     # print('d_o_res', d_o_res)
#     #
#     # for key, value in zip(a_i_k, a_i_v[i]):
#     #     a_i_res.append({"name": key, "value": value})
#     # print('a_i_res', a_i_res)
#     #
#     # for key, value in zip(a_o_k, a_o_v[i]):
#     #     a_o_res.append({"name": key, "value": value})
#     #
#     # print('a_o_res', a_o_res)
#
#     # for i in range(0,len(r_s_d)):
#     #     # print(i)
#     #
#     #     d_i_res.update(dict(zip(d_i_k, d_i_v[i])))
#     #     # print('d_i_v[i]',d_i_v[i])
#     #     d_o_res.update(dict(zip(d_o_k, d_o_v[i])))
#     #     a_i_res.update(dict(zip(a_i_k, a_i_v[i])))
#     #     a_o_res.update(dict(zip(a_o_k, a_o_v[i])))
#
#     # for i in range(0, len(r_s_d)):
#     #     # print(i)
#     #     di = dict(zip(d_i_k, d_i_v[i]))
#     #
#     #     # d_i_res.append({"name": key, "value": value})
#     #
#     #
#     #     d_i_res.update(dict(zip(d_i_k, d_i_v[i])))
#     #     # print('d_i_v[i]',d_i_v[i])
#     #     d_o_res.update(dict(zip(d_o_k, d_o_v[i])))
#     #     a_i_res.update(dict(zip(a_i_k, a_i_v[i])))
#     #     a_o_res.update(dict(zip(a_o_k, a_o_v[i])))
#     # print('d_i_res',d_i_res)
#     result_data=[]
#     # data=[]
#     #
#     # d_i_res = []
#     # d_o_res = []
#     # a_i_res = []
#     # a_o_res = []
#
#     # if not r_s_d:  # If no data available
#     #     entry = {
#     #         "machine_id": r_s_d['machine_id'],
#     #         "machine_location": r_s_d['machine_location'],  # Provide machine location here
#     #         "data": []
#     #     }
#     #     result_data.append(entry)
#     # else:
#
#     for i in range(len(r_s_d)):
#         d_i_res = [{'name': key, 'value': value} for key, value in zip(d_i_k, d_i_v[i])]
#         print('d_i_res',d_i_res)
#         d_o_res = [{'name': key, 'value': value} for key, value in zip(d_o_k, d_o_v[i])]
#         a_i_res = [{'name': key, 'value': value} for key, value in zip(a_i_k, a_i_v[i])]
#         a_o_res = [{'name': key, 'value': value} for key, value in zip(a_o_k, a_o_v[i])]
#
#         # entry = {
#         #     "db_timestamp": r_s_d[i]['db_timestamp'],
#         #     "timestamp": r_s_d[i]['timestamp'],
#         #     "machine_id": r_s_d[i]['machine_id'],
#         #     "machine_location": r_s_d[i]['machine_location'],
#         #     "data": d_i_res + d_o_res + a_i_res + a_o_res
#         # }
#         data_entries = d_i_res + d_o_res + a_i_res + a_o_res
#         print('dtaaaaaaaaaaaaa',data_entries)
#
#
#         entry = {
#             "db_timestamp": r_s_d[i]['db_timestamp'],
#             "timestamp": r_s_d[i]['timestamp'],
#             "machine_id": r_s_d[i]['machine_id'],
#             "machine_location": r_s_d[i]['machine_location'],
#             "data": data_entries
#         }
#         result_data.append(entry)
#
#     # print('d_i_res',d_i_res)
#     # data.append(d_i_res)
#     # data.append(d_o_res)
#     # data.append(a_i_res)
#     # data.append(a_o_res)
#     # print('data',data)
#     #
#     # # print('d_i_res', d_i_res)
#     # # print('d_o_res',d_o_res)
#     # # print('a_i_res',a_i_res)
#     # # print('a_o_res',a_o_res)
#     #
#     # # entry = {
#     # #     "db_timestamp": r_s_d[i]['db_timestamp'],
#     # #     "timestamp": r_s_d[i]['timestamp'],
#     # #     "machine_id": r_s_d[i]['machine_id'],
#     # #     "machine_location": r_s_d[i]['machine_location'],
#     # #     "data": d_i_res + d_o_res + a_i_res + a_o_res
#     # # }
#     # #
#     # # result_data.append(entry)
#
#
#     # for i in range(0,len(r_s_d)):
#     #     r_s_d[i]['digital_input'] = d_i_res
#     #     r_s_d[i]['digital_output'] = d_o_res
#     #     r_s_d[i]['analog_input'] = a_i_res
#     #     r_s_d[i]['analog_output'] = a_o_res
#
#
#     # for i in r_s_d:
#     #     i.update(i.pop("digital_input"))
#     #     i.update(i.pop("digital_output"))
#     #     i.update(i.pop("analog_input"))
#     #     i.update(i.pop("analog_output"))
#
#
#
#
#
#     return JsonResponse({"History":result_data})
#     # return result_data
#     # return r_s_d
#
#
#
