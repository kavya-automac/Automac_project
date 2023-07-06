
from .serializers import *

from Automac_machines_app.serializers import machineSerializer,machineSerializer_two
from Automac_machines_app.models import MachineDetails

def history_fun(machine_id,start_datetime,end_datetime):

    details = MachineDetails.objects.filter(machine_id=machine_id, timestamp__range=[start_datetime, end_datetime])
    print('details',details)
    serializer = machineSerializer(details, many=True)

    r_s_d = serializer.data
    print('r_s_d',r_s_d)

    print('serializer.data', r_s_d[0]['digital_input'])
    d_i_v = []
    d_o_v = []
    a_i_v = []
    a_o_v = []
    for d in range(0,len(r_s_d)):
        d_i_v.append(r_s_d[d]['digital_input'])
        d_o_v.append(r_s_d[d]['digital_output'])
        a_i_v.append(r_s_d[d]['analog_input'])
        a_o_v.append(r_s_d[d]['analog_output'])
    print('d_i_v', d_i_v)
    print('d_o_v', d_o_v)
    print('a_i_v', a_i_v)
    print('a_o_v', a_o_v)
    keys = Machines_List.objects.all()
    serializer_2 = usermachineSerializer(keys, many=True)
    r_s2_d = serializer_2.data
    print('r_s2_d', r_s2_d)

    d_i_k = r_s2_d[0]['digital_input']
    d_o_k = r_s2_d[0]['digital_output']
    a_i_k = r_s2_d[0]['analog_input']
    a_o_k = r_s2_d[0]['analog_output']

    print('d_i_k', d_i_k)
    print('d_o_k', d_o_k)
    print('a_i_k', a_i_k)
    print('a_o_k', a_o_k)


    d_i_res={}
    d_o_res={}
    a_i_res={}
    a_o_res={}
    for i in range(0,len(r_s_d)):
        print(i)
        d_i_res.update(dict(zip(d_i_k,d_i_v[i])))
        print('d_i_v[i]',d_i_v[i])
        d_o_res.update(dict(zip(d_o_k,d_o_v[i])))
        a_i_res.update(dict(zip(a_i_k,a_i_v[i])))
        a_o_res.update(dict(zip(a_o_k,a_o_v[i])))




    print('d_i_res',d_i_res)
    print('d_o_res',d_o_res)
    print('a_i_res',a_i_res)
    print('a_o_res',a_o_res)

    for i in range(0,len(r_s_d)):
        r_s_d[i]['digital_input']=d_i_res
        r_s_d[i]['digital_output']=d_o_res
        r_s_d[i]['analog_input']=a_i_res
        r_s_d[i]['analog_output']=a_o_res

    for i in r_s_d:
        i.update(i.pop("digital_input"))
        i.update(i.pop("digital_output"))
        i.update(i.pop("analog_input"))
        i.update(i.pop("analog_output"))
        i.pop("other")
    return r_s_d



