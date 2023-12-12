import json
from datetime import datetime
from pathlib import Path
import datetime
from django.contrib import messages

from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
# from rest_framework.response import Response
from .serializers import *
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.apps import apps
from . history import history_fun
from Automac_machines_app.serializers import machineSerializer,analog_ip_op_Serializer,kpi_data_Serializer,machineSerializer_two,analog_ip_op_Serializer
# from Automac_machines_app.serializers import *
from Automac_machines_app.models import MachineDetails,Machine_KPI_Data
from . import kpis
# from .Automac_machines_app.models import MachineDetails
from .models import all_Machine_data
# from django.core import serializers
from Automac_machines_app.mqtt import client
from datetime import timedelta


from django.views.decorators.csrf import csrf_exempt

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    print("request.data", request.data)
    print("serializer", serializer)

    # print(User.objects.get(username=request.user.username))
    if serializer.is_valid(raise_exception=True):
        print("if")

        # print(request.user, serializer.validated_data['password'], request.POST, request.GET)
        serializer.save()
        # print("serializer.data",serializer.data)
        return JsonResponse({"status": "Registered"}, status=201)

    # print("****",serializer.errors)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get_user(request):
    userdata=Token.objects.get(key=request.headers['Authorization']).user
    print('userdata',userdata)
    return userdata

@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    print('serializer:', serializer)
    print('serializer_type:', type(serializer))
    if serializer.is_valid():
        print('serializer:', serializer)
        username = serializer.data.get('username')
        # print('serializer_username:', username)
        # print('type_serializer_username:', type(username))
        password = serializer.data.get('password')
        # print('serializer_password:', password)
        # user = User.objects.get(username=username)
        # print(user)
        user = authenticate(username=username, password=password)
        print('authenticate_user:', user)

        if user is not None:
            # login(request, user)
            # print("logged in:", request.user.username)
            token ,_ =Token.objects.get_or_create(user=user)
            login_response = JsonResponse({"status": "user_validated",'generated_token':token.key,'username':username})
            login_response['token'] =str(token.key)

            return login_response
        else:
            return JsonResponse({"status": "unauthorized_user"})
    new_key = 'status'
    error_dict = serializer.errors
    print("error_dict*****", error_dict)
    print("len****", len(error_dict))
    # print(error_dict['password'][0].code)

    # if 'username' and 'password' in error_dict :
    #     # error_dict[new_key] = error_dict.pop('username')
    #     # error_dict[new_key] = error_dict.pop('password')
    #
    #     # return JsonResponse({"status": "username_and_password_cannot_be_empty"})
    if 'username' in error_dict and error_dict['username'][0].code == 'blank' and len(error_dict) == 1:
        # print("len****",len(error_dict))
        print(error_dict['username'][0].code == 'blank')

        error_dict[new_key] = error_dict.pop('username')
        return JsonResponse({"status": error_dict["status"][0]})

    elif 'password' in error_dict and error_dict['password'][0].code == 'blank' and len(error_dict) == 1:
        # print("len****", len(error_dict))
        print(error_dict['password'][0].code == 'blank')
        error_dict[new_key] = error_dict.pop('password')
        return JsonResponse({"status": error_dict["status"][0]})
    elif 'username' in error_dict and error_dict['username'][0].code == 'blank' and 'password' in error_dict and error_dict['password'][0].code == 'blank' and len(error_dict) == 2:
        # print(error_dict["status"][0])
        # print(error_dict.keys())
        return JsonResponse({"status": "username_and_password_cannot_be_empty"})
    # print("sss", serializer.errors.values()[0])
    # return JsonResponse({"status":error_dict["status"][0]})
    # return JsonResponse({"status": "test"})
    # return JsonResponse({"status": error_dict["status"][0]})
    return JsonResponse({"status": "Invalid_Input"})

@api_view(['GET'])
def logout_view(request):
    try:
        current_user = get_user(request)
        print('token of user',current_user.auth_token)
        current_user.auth_token.delete()

        return JsonResponse({"status": "Logged_out"})
    except Token.DoesNotExist:
        return JsonResponse({"status": "Token doesnot exist"})








#session login starts




# @api_view(['POST'])
# def login_view(request):
#     serializer = LoginSerializer(data=request.data)
#     print('serializer:', serializer)
#     print('serializer_type:', type(serializer))
#     if serializer.is_valid():
#         print('serializer:', serializer)
#         username = serializer.data.get('username')
#         # print('serializer_username:', username)
#         # print('type_serializer_username:', type(username))
#         password = serializer.data.get('password')
#         # print('serializer_password:', password)
#         # user = User.objects.get(username=username)
#         # print(user)
#         user = authenticate(username=username, password=password)
#         print('authenticate_user:', user)
#
#         if user is not None:
#             login(request, user)
#             print("logged in:", request.user.username)
#             return JsonResponse({"status": "user_validated",'session_key' : request.session.session_key,"user_name":username})
#
#         else:
#             return JsonResponse({"status": "unauthorized_user"})
#     new_key = 'status'
#     error_dict = serializer.errors
#     print("error_dict*****", error_dict)
#     print("len****", len(error_dict))
#     # print(error_dict['password'][0].code)
#
#     # if 'username' and 'password' in error_dict :
#     #     # error_dict[new_key] = error_dict.pop('username')
#     #     # error_dict[new_key] = error_dict.pop('password')
#     #
#     #     # return JsonResponse({"status": "username_and_password_cannot_be_empty"})
#     if 'username' in error_dict and error_dict['username'][0].code == 'blank' and len(error_dict) == 1:
#         # print("len****",len(error_dict))
#         print(error_dict['username'][0].code == 'blank')
#
#         error_dict[new_key] = error_dict.pop('username')
#         return JsonResponse({"status": error_dict["status"][0]})
#
#     elif 'password' in error_dict and error_dict['password'][0].code == 'blank' and len(error_dict) == 1:
#         # print("len****", len(error_dict))
#         print(error_dict['password'][0].code == 'blank')
#         error_dict[new_key] = error_dict.pop('password')
#         return JsonResponse({"status": error_dict["status"][0]})
#     elif 'username' in error_dict and error_dict['username'][0].code == 'blank' and 'password' in error_dict and error_dict['password'][0].code == 'blank' and len(error_dict) == 2:
#         # print(error_dict["status"][0])
#         # print(error_dict.keys())
#         return JsonResponse({"status": "username_and_password_cannot_be_empty"})
#     # print("sss", serializer.errors.values()[0])
#     # return JsonResponse({"status":error_dict["status"][0]})
#     # return JsonResponse({"status": "test"})
#     # return JsonResponse({"status": error_dict["status"][0]})
#     return JsonResponse({"status": "Invalid_Input"})


# @csrf_exempt
# @api_view(['GET'])
# @authentication_classes([SessionAuthentication])
# @permission_classes([IsAuthenticated])

# def my_data_view_username(request):
#     BASE_DIR = Path(__file__).resolve().parent.parent
    # Only authenticated users with a valid session ID can access this endpoint.
    # Access the user's data here and return it in the response.
    # user = User.objects.get(username=username)
    # print(user)
    # session_id = request.session.session_key
    # print(session_id,":*********")
    # Validate session ID and retrieve data for authenticated user
    # if request.session.session_key :
    #     print("request", request.method, request.POST, request.GET,request.session.session_key,request.session)
    #
    #     print("username:",request.user.username)
    # data = {
    #     'username': request.user.username,
    #     # 'email': request.user.email,
    #     # Add any other data fields you want to expose.
    # }
    # return Response(data)
    # data = json.load(open(str(BASE_DIR) + "/Automac_app/dashboard.json"))
    # return JsonResponse(data)
    # return JsonResponse({'message': ' session id needed .'})


# @csrf_exempt




#logout starts


# @api_view(['GET'])
# # @authentication_classes([SessionAuthentication])
# # @permission_classes([IsAuthenticated])
# def logout_view(request):
#     print("entering logout")
#     print("loggedout", request.user.username)
#
#     logout(request)
#     return JsonResponse({"status": "Logged_out"})

#convert list or dict values into string


@authentication_classes([SessionAuthentication])
# @permission_classes([IsAuthenticated])
# @login_required(login_url='login_view')
class Dashboard(ViewSet):
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        try:
            current_user = get_user(request)

            if current_user.is_authenticated:
                current_time = datetime.datetime.now()
                print('current_time', current_time)

                # current_time = datetime.datetime.now()

                today = datetime.datetime.now().date()
                user_machine_kpi = all_Machine_data.objects.filter(user_name__username=current_user).values('machine_id__machine_id') \
                    .distinct('machine_id__machine_id', 'plant_name__plant_name', 'model_name__model_name')
                result = []
                machine_count=0
                inactive_count=0
                active_count=0
                for m_id in user_machine_kpi:
                    machines = m_id['machine_id__machine_id']
                    machine_count += 1

                    if MachineDetails.objects.filter(machine_id=machines).exists():

                        # to_fetch_lastrecord_data = MachineDetails.objects.filter(machine_id=machines).values('machine_id','timestamp').latest('timestamp')
                        to_fetch_lastrecord_data = MachineDetails.objects.filter(machine_id=machines).values('machine_id','timestamp')
                        fetch_latest=to_fetch_lastrecord_data.latest('timestamp')

                        print('to_fetch_lastrecord_data',to_fetch_lastrecord_data)
                        print('fetch_latest',fetch_latest)
                        last_record_time1 = fetch_latest['timestamp']

                        last_record_time2 = last_record_time1.strftime("%Y-%m-%d %H:%M:%S.%f %Z")
                        last_record_time = datetime.datetime.strptime(last_record_time2,"%Y-%m-%d %H:%M:%S.%f %Z")

                        print('last_record_time',last_record_time)
                        print('current_time',current_time)


                        time_difference = abs((current_time - last_record_time).total_seconds())
                        # time_difference = current_time - last_record_time
                        print('time_difference',time_difference)
                        print(' time_difference > timedelta(seconds=30)', time_difference > 60)

                        if time_difference > 60:
                        # if time_difference > timedelta(seconds=30):

                            machine_status = "inactive"
                            inactive_count+=1
                            print('inactive if',inactive_count)

                        else:

                            machine_status = "active"
                            active_count+=1
                            print('active else',active_count)


                    else:
                        inactive_count += 1
                        print('inactive else',inactive_count)



                    count_card_data = {
                        "title": "count_card",
                        "machine_count": str(machine_count),
                        "inactive_count": str(inactive_count),
                        "active_count": str(active_count)
                    }
                    # type = "Min_Max_values"
                    final_data = {}
                    type = "production_difference"
                    get_kpi_type = Machine_KPI_Data.objects.filter(machine_id=machines,
                                                                   kpi_id__kpi_inventory_id__Kpi_Type=type,
                                                                   timestamp__date=today)

                    print('get_kpi_type',get_kpi_type)
                    value_list = ["0"]
                    kpi_name = ""
                    for kpi in get_kpi_type:

                        kpi_name=kpi.kpi_id.kpi_name
                        print('kpi_name',kpi_name)
                        # if kpi_name:
                        #     break
                        # # kpiname.append(kpi_name)
                        # # print('kpiname',kpiname)

                        value_list = kpi.kpi_data
                        print("value_list",value_list)
                    # print('kpiname',kpiname)
                    result.append({"machine": machines, "values": value_list})
                    final_data = {"title": "bar_graph", "name": kpi_name, "data": result}

                return JsonResponse({"count_card_data":count_card_data,"bar_graph":final_data})

        except Token.DoesNotExist:
            print("else")
            return JsonResponse({"status": "login_required"})


# @authentication_classes([SessionAuthentication])
# @permission_classes([IsAuthenticated])
class MachinesView(ViewSet):
    @action(detail=False, methods=['get'])
    def machine_list(self, request):
        try:
            # if request.user.is_authenticated:
            print('requesttttttt',request.META)



            # print('requesttttttt',request.META)
            # machine_id='ABD2'
            # machine=Machines_List.objects.get(machine_id=machine_id)
            # io=IO_List.objects.filter(machine_id__machine_id=machine).order_by('id')
            # inputs=[]
            # for i in io:
            #     inputs.append(i.IO_type)
            #
            # print('...................',inputs)
            #



            # print('userssss', request.user)
            user_data=get_user(request)
            print('user_data',user_data)

            unique_data=all_Machine_data.objects.filter(user_name__username=user_data).values('machine_id__machine_id','plant_name__plant_name','model_name__model_name','company_name__company_name','line_name__line_name','machine_id__machine_name')\
                .distinct('machine_id__machine_id','plant_name__plant_name','model_name__model_name')
            # unique_data=all_Machine_data.objects.values('machine_id','plant_name','model_name','company_name','line_name')

            print('unique_data',unique_data)

            unique_data_json =json.dumps(list(unique_data))
            unique_machine_data=json.loads(unique_data_json)
            # unique_data_json =serializers.serialize('json',unique_data)
            print('unique_data_json',unique_data_json)
            print('unique_machine_data',unique_machine_data)

            machine_list_data=[]
            # # for data in get_user_data_s_data:
            # #     machine_id=data.plant_name.plant_name if get_user_data[ i].plant_name is not None else "None"
            print("--------------------> ",unique_machine_data[0]['line_name__line_name'])
            for i in range(0,len(unique_machine_data)):
                machine_id = unique_machine_data[i]['machine_id__machine_id'] if unique_machine_data[
                                                                                 i]['machine_id__machine_id'] is not None else "None"
                company_name = unique_machine_data[i]['company_name__company_name'] if unique_machine_data[
                                                                                 i]['company_name__company_name'] is not None else "None"
                plant_name = unique_machine_data[i]['plant_name__plant_name'] if unique_machine_data[
                                                                           i]['plant_name__plant_name'] is not None else "None"
                model_name = unique_machine_data[i]['model_name__model_name'] if unique_machine_data[
                                                                           i]['model_name__model_name'] is not None else "None"
                line_name = unique_machine_data[i]['line_name__line_name'] if unique_machine_data[i]['line_name__line_name'] is not None else "None"
                machine_name = unique_machine_data[i]['machine_id__machine_name'] if unique_machine_data[
                                                                               i]['machine_id__machine_name'] is not None else "None"


                machine_list_data.append({
                        "company_name": company_name,
                        "plant_name": plant_name,
                        "machine_id": machine_id,
                        "model_name": model_name,
                        "line_name": line_name,
                        "machine_name": machine_name
                    })
                print('machine_list_data',machine_list_data)

            #

                #
                # get_user_data[i].machine_id.machine_id
                #
                # get_user_data_s_data[i].update(company_name=get_user_data[i].company_name.company_name)
                # get_user_data_s_data[i].update(plant_name=get_user_data[i].plant_name.plant_name)
                # get_user_data_s_data[i].update(model_name=get_user_data[i].model_name.model_name)
                # get_user_data_s_data[i].update(machine_id=get_user_data[i].machine_id.machine_id)
                # # get_user_data_s_data[i].update(machine_id=get_user_data[i].machine_id.machine_location)
                # get_user_data_s_data[i].update(line_name=str(get_user_data[i].line_name))
                # # print('get_user_data_s_data',get_user_data_s_data)
                # get_user_data_s_data[i]['machine_name']=get_user_data[i].machine_id.machine_name


            return JsonResponse({"machine_list": machine_list_data})

        except Token.DoesNotExist:
            return JsonResponse({"status": "login_required"})

        # else:
        #     print('requesttttt',request.META)
        #     print("else")
        #     return JsonResponse({"status": "login_required"})

    @action(detail=False, method=["get"])
    # @action(detail=False, method=["get","post"])
    def machine_details(self, request):
        try:
            current_user = get_user(request)

            if current_user.is_authenticated:
                print("if")
                BASE_DIR = Path(__file__).resolve().parent.parent

                machine_id=request.query_params.get('machine_id')
                # d=Machines_List.objects.filter(machine_id=machine_id)

                print("request", request.method, request.POST, request.GET)
                # print("request.method",request.GET['id'])
                # q=Machines_List.objects.filter(id=id).values('id','machine_name','machine_location','date_of_installation')
                # print('q',q)

                if "machine_id" in request.GET and "module" in request.GET:
                    module = request.GET["module"]

                    # @action(detail=False, method=["get"])
                    # def documents(self, request):
                    #     fields = [
                    #         {
                    #
                    #         }
                    #     ]
                    if module == "Details":
                        # id = request.query_params.get('id')

                        general_data = Machines_List.objects.get(machine_id=machine_id)
                        print('general_data',general_data)
                        general_serialzer=generalmachineSerializer(general_data)
                        general_serialzer_data_11=general_serialzer.data
                        # print('general_serialzer',general_serialzer_data_11)
                        general_serialzer_data_1=null_to_str(general_serialzer_data_11)
                        print('general_serialzer_data_1',general_serialzer_data_1)

                        plant_line_data=all_Machine_data.objects.filter(machine_id=general_data.id,user_name__username=current_user)
                        # plant_line_data=all_Machine_data.objects.filter(machine_id=general_data.id,user_name=request.user)
                        print('plant_line_data',plant_line_data)

                        if not plant_line_data.exists():
                            # If the plant_line_data is empty, return a response indicating that the user doesn't have access.
                            return JsonResponse({"message": "User does not have access to this machine."}, status=403)


                        s_data=all_Machine_data_Serializer(plant_line_data,many=True)
                        s_data_d=s_data.data
                        print('plant_line_data',plant_line_data[0].plant_name,type(plant_line_data))

                        for f_names in range(0,len(plant_line_data)):
                            if plant_line_data[f_names] is not None:
                                s_data_d[f_names].update(
                                    plant_name=plant_line_data[f_names].plant_name.plant_name if plant_line_data[
                                                                                                     f_names].plant_name is not None else "None")
                                s_data_d[f_names].update(
                                    model_name=plant_line_data[f_names].model_name.model_name if plant_line_data[
                                                                                                     f_names].model_name is not None else "None")
                                s_data_d[f_names].update(
                                    line_name=str(plant_line_data[f_names].line_name) if plant_line_data[
                                                                                             f_names].line_name is not None else "None")
                                print('s_data', s_data_d)
                                general_serialzer_data_1.update(dict(s_data_d[0]))
                                # general_serialzer_data_1 = dict(s_data_d)

                        if not s_data_d:
                            return JsonResponse({"general_data": general_serialzer_data_1})
                        #     s_data_d[f_names].update(plant_name=plant_line_data[f_names].plant_name.plant_name)
                        #     s_data_d[f_names].update(model_name=plant_line_data[f_names].model_name.model_name)
                        #     s_data_d[f_names].update(line_name=str(plant_line_data[f_names].line_name))
                        #     print('s_data',s_data_d)
                        #     general_serialzer_data_1.update(dict(s_data_d[0]))
                        #     # general_serialzer_data_1=dict(s_data_d)
                        # if not s_data_d:
                        #     return JsonResponse({"general_data": general_serialzer_data_1})

                        Manuals_and_Docs=[{"Document_name":"Electrical_Drawing",
                                           "Uploaded_by":"harsha",
                                           "Date":"27/07/2023",
                                           "Url":"https://datasheets.raspberrypi.com/rpi4/raspberry-pi-4-product-brief.pdf"}]
                        Techincal_Details=[{
                            "Date":"27/07/2023",
                            "Device_name":"Compressor",
                            "Make":"ELGI",
                            "Model_No":"ELGI001",
                            "Label":"label"

                        },{
                            "Date": "27/07/2023",
                            "Device_name": "Cooler",
                            "Make": "CROMPTON",
                            "Model_No": "CRMP234",
                            "Label": "label"

                        }
                        ]



                        data = {'general_details':general_serialzer_data_1,'Manuals_and_Docs':Manuals_and_Docs,'Techincal_Details':Techincal_Details}
                        # data = json.load(open(str(BASE_DIR)+"/Automac_app/machine_details.json"))

                    elif module == "kpis":
                        try:
                            machine = Machines_List.objects.get(machine_id=machine_id)
                            print('machineeeeeeeee',machine)
                            print('machineenameee',machine.machine_id)
                        except Machines_List.DoesNotExist:
                            error_message = "Please enter a valid machine_id."
                            return JsonResponse({"status": error_message}, status=400)  # Return an error response

                        # user=request.query_params.get('user')
                        user=current_user
                        print('userrrr',user)

                        data = kpis.get_kpis_data(user,machine)
                        data['machine_id']=machine.machine_id
                        data['machine_name']=machine.machine_name





                        # data = json.load(open(str(BASE_DIR)+"/Automac_app/machine_details(kpis).json"))

                    elif module == "iostatus":
                        try:
                            machine = Machines_List.objects.get(machine_id=machine_id)
                        except Machines_List.DoesNotExist:
                            error_message = "Please enter a valid machine_id."
                            return JsonResponse({"status": error_message}, status=400)  # Return an error response

                        # print('machime.............',machine_id)
                        # print('m_nameeeeeeeeeee.............',machine.machine_name)

                        input_output_data = IO_List.objects.filter(machine_id=machine.id).order_by('id')
                        # print('input_output_data', input_output_data)
                        input_output_data_serializer = IO_list_serializer(input_output_data, many=True)
                        # print('input_output_data_serializer', input_output_data_serializer.data)
                        input_output_data_serializer_data=input_output_data_serializer.data
                        # print('type', input_output_data_serializer_data)
                        # print('name', input_output_data_serializer_data[0]['IO_name'])
                        # print('color', input_output_data_serializer_data[0].IO_color)
                        digital_input_keys=[]
                        digital_output_keys=[]
                        analog_input_keys=[]
                        analog_output_keys=[]
                        other_keys=[]
                        color = []
                        values = []

                        for i in range(len(input_output_data)):
                            # print('iiiiiiiiiii',i)
                            if input_output_data_serializer_data[i]['IO_type'] == "analog_output":
                                analog_output_keys.append(input_output_data_serializer_data[i]['IO_name'])

                            if input_output_data_serializer_data[i]['IO_type'] == "analog_input":
                                analog_input_keys.append(input_output_data_serializer_data[i]['IO_name'])
                            if input_output_data_serializer_data[i]['IO_type'] == "digital_output":
                                digital_output_keys.append(input_output_data_serializer_data[i]['IO_name'])

                            if input_output_data_serializer_data[i]['IO_type']=="digital_input":
                                # print('iiiiiiiiiiiiiiiiiiiii',i ,input_output_data_serializer_data[i]['IO_name'])
                                digital_input_keys.append(input_output_data_serializer_data[i]['IO_name'])
                            if input_output_data_serializer_data[i]['IO_type']=="other":
                                # print('iiiiiiiiiiiiiiiiiiiii',i ,input_output_data_serializer_data[i]['IO_name'])
                                other_keys.append(input_output_data_serializer_data[i]['IO_name'])
                        print('digital_input_keys',digital_input_keys)
                        print('digital_output_keys',digital_output_keys)
                        print('analog_input_keys',analog_input_keys)
                        print('analog_output_keys',analog_output_keys)
                        print('color',color)
                        print('values',values)


                        machine_values_data = MachineDetails.objects.filter(machine_id=machine.machine_id).order_by('-timestamp').first()
                        # print('machine_values_data', machine_values_data)
                        last_valies_data_1 = machineSerializer(machine_values_data)
                        last_valies_data = last_valies_data_1.data
                        print('last_valies_data',last_valies_data)




                        digital_keyvalue_input_data=[]

                        for key, value in zip(digital_input_keys, last_valies_data.get('digital_input', [])):

                            value_str = "On" if value else "Off"
                            color=None
                            for i in range(len(input_output_data)):
                                if input_output_data_serializer_data[i]['IO_type'] == "digital_input" and input_output_data_serializer_data[i]['IO_name'] == key:
                                    db_color = input_output_data_serializer_data[i]['IO_color']
                                    color = db_color[0] if value else db_color[1]
                                    break  # Exit loop once the correct key is found
                                else:
                                    pass

                            digital_keyvalue_input_data.append({"name": key, "value": value_str,"color":color})
                        # print('digital_keyvalue_input_data',digital_keyvalue_input_data)


                        digital_keyvalue_output_data=[]
                        for key, value in zip(digital_output_keys, last_valies_data.get('digital_output', [])):
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


                            digital_keyvalue_output_data.append({"name": key, "value": value_str,"color":color})
                        # print('digital_keyvalue_output_data', digital_keyvalue_output_data)

                        analog_keyvalue_input_data=[]
                        for key, value in zip(analog_input_keys, last_valies_data.get('analog_input', [])):
                            db_unit=None
                            for i in range(len(input_output_data)):
                                if input_output_data_serializer_data[i]['IO_type'] == "analog_input" and \
                                        input_output_data_serializer_data[i]['IO_name'] == key:
                                    db_unit = input_output_data_serializer_data[i]['IO_Unit']
                                    color= input_output_data_serializer_data[i]['IO_color'][0]
                                    break  # Exit loop once the correct key is found
                                else:
                                    pass

                            analog_keyvalue_input_data.append({"name": key, "value": str(value),"color":color,"unit":db_unit})
                        # print('analog_keyvalue_input_data', analog_keyvalue_input_data)

                        analog_keyvalue_output_data = []
                        for key, value in zip(analog_output_keys, last_valies_data.get('analog_output', [])):
                            db_unit = None
                            for i in range(len(input_output_data)):
                                if input_output_data_serializer_data[i]['IO_type'] == "analog_output" and \
                                        input_output_data_serializer_data[i]['IO_name'] == key:
                                    db_unit = input_output_data_serializer_data[i]['IO_Unit']
                                    color= input_output_data_serializer_data[i]['IO_color'][0]

                                    break  # Exit loop once the correct key is found
                                else:
                                    pass

                            analog_keyvalue_output_data.append({"name": key, "value": str(value),"color":color,"unit":db_unit})
                        # print('analog_keyvalue_output_data', analog_keyvalue_output_data)
                        # print('timeeeeeeeeeeeeeeeeeeeeee',str(last_valies_data.get('timestamp',datetime.datetime.now())))
                        others_keyvalue_input_data = []
                        for key, value in zip(other_keys, last_valies_data.get('other', [])):
                            db_unit = None
                            for i in range(len(input_output_data)):
                                if input_output_data_serializer_data[i]['IO_type'] == "other" and \
                                        input_output_data_serializer_data[i]['IO_name'] == key:
                                    db_unit = input_output_data_serializer_data[i]['IO_Unit']
                                    color = input_output_data_serializer_data[i]['IO_color'][0]
                                    break  # Exit loop once the correct key is found
                                else:
                                    pass

                            others_keyvalue_input_data.append(
                                {"name": key, "value": str(value), "color": color, "unit": db_unit})
                        # print('analog_keyvalue_input_data', analog_keyvalue_input_data)

                        timestamp = last_valies_data.get('timestamp')
                        if timestamp:
                            formatted_time = str(timestamp)
                        else:
                            formatted_time = "0000-00-00T00:00:00Z"#change
                            # formatted_time = str(datetime.datetime.now())
                        print('formatted_time',formatted_time)

                        data = {'iostatus': {
                            "machine_id":machine.machine_id,
                            "machine_name":machine.machine_name,
                            "digital_input":digital_keyvalue_input_data,
                            "digital_output":digital_keyvalue_output_data,
                            "analog_input":analog_keyvalue_input_data,
                            "analog_output":analog_keyvalue_output_data,
                            "others":others_keyvalue_input_data,
                            "db_timestamp": formatted_time

                        }}
            #------------------------ ADDING CONTROL CODE

            # --------------------code starts here------------------




                    elif module == "control":
                        try:
                            machine = Machines_List.objects.get(machine_id=machine_id)
                        except Machines_List.DoesNotExist:
                            error_message = "Please enter a valid machine_id."
                            return JsonResponse({"status": error_message}, status=400)  # Return an error response

                        # print('machime.............',machine_id)
                        # print('m_nameeeeeeeeeee.............',machine.machine_name)

                        input_output_data = IO_List.objects.filter(machine_id=machine.id).order_by('id')
                        # print('input_output_data', input_output_data)
                        input_output_data_serializer = IO_list_serializer(input_output_data, many=True)
                        # print('input_output_data_serializer', input_output_data_serializer.data)
                        input_output_data_serializer_data=input_output_data_serializer.data
                        # print('type', input_output_data_serializer_data)
                        # print('name', input_output_data_serializer_data[0]['IO_name'])
                        # print('color', input_output_data_serializer_data[0].IO_color)
                        digital_input_keys=[]
                        digital_output_keys=[]
                        analog_input_keys=[]
                        analog_output_keys=[]
                        color = []
                        values = []

                        for i in range(len(input_output_data)):
                            # print('iiiiiiiiiii',i)
                            if input_output_data_serializer_data[i]['IO_type'] == "analog_output":
                                analog_output_keys.append(input_output_data_serializer_data[i]['IO_name'])

                            if input_output_data_serializer_data[i]['IO_type'] == "analog_input":
                                analog_input_keys.append(input_output_data_serializer_data[i]['IO_name'])
                            if input_output_data_serializer_data[i]['IO_type'] == "digital_output":
                                digital_output_keys.append(input_output_data_serializer_data[i]['IO_name'])

                            if input_output_data_serializer_data[i]['IO_type']=="digital_input":
                                # print('iiiiiiiiiiiiiiiiiiiii',i ,input_output_data_serializer_data[i]['IO_name'])
                                digital_input_keys.append(input_output_data_serializer_data[i]['IO_name'])
                        print('digital_input_keys',digital_input_keys)
                        print('digital_output_keys',digital_output_keys)
                        print('analog_input_keys',analog_input_keys)
                        print('analog_output_keys',analog_output_keys)
                        print('color',color)
                        print('values',values)


                        machine_values_data = MachineDetails.objects.filter(machine_id=machine.machine_id).order_by('-timestamp').first()
                        # print('machine_values_data', machine_values_data)
                        last_valies_data_1 = machineSerializer(machine_values_data)
                        last_valies_data = last_valies_data_1.data
                        print('last_valies_data',last_valies_data)




                        digital_keyvalue_input_data=[]

                        for key, value in zip(digital_input_keys, last_valies_data.get('digital_input', [])):

                            value_str = "On" if value else "Off"
                            color=None
                            for i in range(len(input_output_data)):
                                if input_output_data_serializer_data[i]['IO_type'] == "digital_input" and input_output_data_serializer_data[i]['IO_name'] == key:
                                    db_color = input_output_data_serializer_data[i]['IO_color']
                                    color = db_color[0] if value else db_color[1]
                                    break  # Exit loop once the correct key is found
                                else:
                                    pass

                            digital_keyvalue_input_data.append({"name": key, "value": value_str,"color":color})
                        # print('digital_keyvalue_input_data',digital_keyvalue_input_data)


                        digital_keyvalue_output_data=[]
                        for key, value in zip(digital_output_keys, last_valies_data.get('digital_output', [])):
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


                            digital_keyvalue_output_data.append({"name": key, "value": value_str,"color":color})
                        # print('digital_keyvalue_output_data', digital_keyvalue_output_data)

                        analog_keyvalue_input_data=[]
                        for key, value in zip(analog_input_keys, last_valies_data.get('analog_input', [])):
                            db_unit=None
                            for i in range(len(input_output_data)):
                                if input_output_data_serializer_data[i]['IO_type'] == "analog_input" and \
                                        input_output_data_serializer_data[i]['IO_name'] == key:
                                    db_unit = input_output_data_serializer_data[i]['IO_Unit']
                                    color= input_output_data_serializer_data[i]['IO_color'][0]
                                    break  # Exit loop once the correct key is found
                                else:
                                    pass

                            analog_keyvalue_input_data.append({"name": key, "value": str(value),"color":color,"unit":db_unit})
                        # print('analog_keyvalue_input_data', analog_keyvalue_input_data)

                        analog_keyvalue_output_data = []
                        for key, value in zip(analog_output_keys, last_valies_data.get('analog_output', [])):
                            db_unit = None
                            for i in range(len(input_output_data)):
                                if input_output_data_serializer_data[i]['IO_type'] == "analog_output" and \
                                        input_output_data_serializer_data[i]['IO_name'] == key:
                                    db_unit = input_output_data_serializer_data[i]['IO_Unit']
                                    color= input_output_data_serializer_data[i]['IO_color'][0]

                                    break  # Exit loop once the correct key is found
                                else:
                                    pass

                            analog_keyvalue_output_data.append({"name": key, "value": str(value),"color":color,"unit":db_unit})
                        # print('analog_keyvalue_output_data', analog_keyvalue_output_data)
                        # print('timeeeeeeeeeeeeeeeeeeeeee',str(last_valies_data.get('timestamp',datetime.datetime.now())))
                        timestamp = last_valies_data.get('timestamp')
                        if timestamp:
                            formatted_time = str(timestamp)
                        else:
                            formatted_time = str(datetime.datetime.now())
                        print('formatted_time',formatted_time)

                        data = {'control': {
                            "machine_id":machine.machine_id,
                            "machine_name":machine.machine_name,
                            "digital_output":digital_keyvalue_output_data,
                            "db_timestamp": formatted_time

                        }}

                    else:
                        data = {
                            'status': 'please_enter_correct_module_name'
                        }
                else:
                    data = {
                        'status': 'enter_correct_id_and_module'
                    }
                return JsonResponse(data)
            else:
                return JsonResponse({"status": "login_required"})
        except Token.DoesNotExist:
            return JsonResponse({"status" : "login_required"})


@csrf_exempt
@api_view(['PUT'])
def machine_control(request):
    print('******',request.data)

    machine_id=request.data.get('machine_id')
    name=request.data.get('name')
    value=request.data.get('value')
    machine = Machines_List.objects.get(machine_id=machine_id)
    input_output_data = IO_List.objects.filter(machine_id=machine.id,IO_type='digital_output').order_by('id').values_list('IO_name',flat=True)
    output = list(input_output_data).index(name)
    print('index***********',list(input_output_data).index(name))
    print('input_output_data----------',input_output_data)
    print('machine_id,name,value', machine_id,name,value)

    control_json = {"mid":machine_id, "data":{"output":output, "value":value}}
    client.publish("ieee/control", json.dumps(control_json))
    # return JsonResponse({"status":list(input_output_data).index(name)})
    return JsonResponse({"status":"data has been sent"})






# def testing_sessions(request):
#     if request.user.is_authenticated:
#         session_key = request.session.session_key
#         print("Session Key:", session_key)
#
#         request.session['dummy_data'] = 'Hello, World!'
#         json_data_1=json.dumps({"name":"kavya","company":"Automac"})
#         request.session['json_data'] =json_data_1
#         # messages.success(request, 'Dummy data successfully stored in session.')
#         dummy = request.session.get('dummy_data')
#         json_data = request.session.get('json_data')
#         print("Dummy Data:", dummy)
#         print("json data:", json_data)
#
#         # messages.warning(request, 'warning.')
#
#     else:
#         pass

@authentication_classes([SessionAuthentication])
# @permission_classes([IsAuthenticated])
class Trails(ViewSet):
    @action(detail=False, method=['get'])
    def Trail_details(self,request):
        try:
            current_user = get_user(request)
            if current_user.is_authenticated:
                print("if")
                # data_session=testing_sessions(request)
                # print('data_session',data_session)

                machine_id = request.GET.get('machine_id')
                date = request.GET.get('date')
                # end_datetime = request.GET.get('end_datetime')
                print('request',request.method,request.GET)
                # user="user1"
                # print('.............user',user)

                trail_detail_data = history_fun(machine_id,date)
                # reports_data = history_fun(machine_id,start_datetime,end_datetime)
                return trail_detail_data

            else:
                print("else")
                return JsonResponse({"status": "login_required"})
        except Token.DoesNotExist:
            return JsonResponse({"status": "login_required"})



    @action(detail=False, method=['get'])
    def Trail_List(self, request):
        try:
            current_user = get_user(request)

            if current_user.is_authenticated:
                print("if")

                BASE_DIR = Path(__file__).resolve().parent.parent

                unique_data = all_Machine_data.objects.filter(user_name__username=current_user).values('machine_id__machine_id',
                                                                                             'plant_name__plant_name',
                                                                                             'model_name__model_name',
                                                                                             'company_name__company_name',
                                                                                             'line_name__line_name',
                                                                                             'machine_id__machine_name') \
                    .distinct('machine_id__machine_id', 'plant_name__plant_name', 'model_name__model_name')
                # unique_data=all_Machine_data.objects.values('machine_id','plant_name','model_name','company_name','line_name')

                print('unique_data', unique_data)

                unique_data_json = json.dumps(list(unique_data))
                unique_machine_data = json.loads(unique_data_json)
                # unique_data_json =serializers.serialize('json',unique_data)
                print('unique_data_json', unique_data_json)
                print('unique_machine_data', unique_machine_data)

                trail_list_data = []
                # # for data in get_user_data_s_data:
                # #     machine_id=data.plant_name.plant_name if get_user_data[ i].plant_name is not None else "None"
                print("--------------------> ", unique_machine_data[0]['line_name__line_name'])
                for i in range(0, len(unique_machine_data)):
                    machine_id = unique_machine_data[i]['machine_id__machine_id'] if unique_machine_data[
                                                                                         i][
                                                                                         'machine_id__machine_id'] is not None else "None"
                    company_name = unique_machine_data[i]['company_name__company_name'] if unique_machine_data[
                                                                                               i][
                                                                                               'company_name__company_name'] is not None else "None"
                    plant_name = unique_machine_data[i]['plant_name__plant_name'] if unique_machine_data[
                                                                                         i][
                                                                                         'plant_name__plant_name'] is not None else "None"
                    model_name = unique_machine_data[i]['model_name__model_name'] if unique_machine_data[
                                                                                         i][
                                                                                         'model_name__model_name'] is not None else "None"
                    line_name = unique_machine_data[i]['line_name__line_name'] if unique_machine_data[i][
                                                                                      'line_name__line_name'] is not None else "None"
                    machine_name = unique_machine_data[i]['machine_id__machine_name'] if unique_machine_data[
                                                                                             i][
                                                                                             'machine_id__machine_name'] is not None else "None"

                    trail_list_data.append({
                        "company_name": company_name,
                        "plant_name": plant_name,
                        "machine_id": machine_id,
                        "model_name": model_name,
                        "line_name": line_name,
                        "machine_name": machine_name
                    })
                    print('machine_list_data', trail_list_data)


                return JsonResponse({"Trail_list": trail_list_data})



            else:
                print("else")
                return JsonResponse({"status":"login_required"})

        except Token.DoesNotExist:
            return JsonResponse({"status": "login_required"})


# @authentication_classes([SessionAuthentication])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])

class ReportsView(ViewSet):
    @action(detail=False, method=['get'])
    def Report_List(self, request):
        try:
            current_user =get_user(request)
            print('current_user',current_user)
            if current_user.is_authenticated:
                print("if")

                BASE_DIR = Path(__file__).resolve().parent.parent

                unique_data = all_Machine_data.objects.filter(user_name__username=current_user).values('machine_id__machine_id',
                                                                                             'plant_name__plant_name',
                                                                                             'model_name__model_name',
                                                                                             'company_name__company_name',
                                                                                             'line_name__line_name',
                                                                                             'machine_id__machine_name','kpi__kpi_name') \
                    .distinct('machine_id__machine_id', 'plant_name__plant_name', 'model_name__model_name')
                # unique_data=all_Machine_data.objects.values('machine_id','plant_name','model_name','company_name','line_name')

                print('unique_data', unique_data)

                unique_data_json = json.dumps(list(unique_data))
                unique_machine_data = json.loads(unique_data_json)
                # unique_data_json =serializers.serialize('json',unique_data)
                print('unique_data_json', unique_data_json)
                print('unique_machine_data', unique_machine_data)

                report_list_data = []
                # # for data in get_user_data_s_data:
                # #     machine_id=data.plant_name.plant_name if get_user_data[ i].plant_name is not None else "None"
                print("--------------------> ", unique_machine_data[0]['line_name__line_name'])
                for i in range(0, len(unique_machine_data)):
                    machine_id = unique_machine_data[i]['machine_id__machine_id'] if unique_machine_data[
                                                                                         i][
                                                                                         'machine_id__machine_id'] is not None else "None"
                    company_name = unique_machine_data[i]['company_name__company_name'] if unique_machine_data[
                                                                                               i][
                                                                                               'company_name__company_name'] is not None else "None"
                    plant_name = unique_machine_data[i]['plant_name__plant_name'] if unique_machine_data[
                                                                                         i][
                                                                                         'plant_name__plant_name'] is not None else "None"
                    model_name = unique_machine_data[i]['model_name__model_name'] if unique_machine_data[
                                                                                         i][
                                                                                         'model_name__model_name'] is not None else "None"
                    line_name = unique_machine_data[i]['line_name__line_name'] if unique_machine_data[i][
                                                                                      'line_name__line_name'] is not None else "None"
                    machine_name = unique_machine_data[i]['machine_id__machine_name'] if unique_machine_data[
                                                                                             i][
                                                                                             'machine_id__machine_name'] is not None else "None"

                    reportsss = all_Machine_data.objects.filter(user_name__username="user1",machine_id__machine_id=machine_id)
                    machine_all_reports = []

                    for k in reportsss:
                        data = k.kpi.kpi_name if k.kpi is not None else "None"
                        print('dataaaaaaaaaaaaaaaa', data)
                        machine_all_reports.append(data)


                    report_list_data.append({
                        "report_type":machine_all_reports,
                        "company_name": company_name,
                        "plant_name": plant_name,
                        "machine_id": machine_id,
                        "model_name": model_name,
                        "line_name": line_name,
                        "machine_name": machine_name
                    })
                    print('machine_list_data', report_list_data)


                return JsonResponse({"report": report_list_data})



            else:
                print("else")
                return JsonResponse({"status":"login_required"})
        except Token.DoesNotExist:
            return JsonResponse({"status": "login_required"})





    @action(detail=False, methods=['post'])
    def Reports(self, request):
        try:
            current_user = get_user(request)
            if current_user.is_authenticated:
                try:#remove try and except for next push
                    request_data = request.data
                    print('request_data',request_data)
                except json.JSONDecodeError:
                    return JsonResponse({"error": "Invalid JSON data."}, status=status.HTTP_400_BAD_REQUEST)

                # Extract user-selected parameters
                kpi_name = request.data.get('report_type')
                machine_id = request.data.get('machine_id')
                start_datetime = request.data.get('start_datetime')
                end_datetime1 = request.data.get('end_datetime')
                # start_datetime = datetime.strptime(start_datetime1,'%Y-%m-%d %H:%M:%S')
                # end_datetime = datetime.strptime(end_datetime1,'%Y-%m-%d %H:%M:%S')

                print('.........................' ,end_datetime1)

                if not kpi_name or not machine_id or not start_datetime or not end_datetime1:
                    return JsonResponse({"error": "kpi_name, machine_id, start_datetime, and end_datetime are required."},
                                        status=status.HTTP_400_BAD_REQUEST)

                try:
                    # Convert the start_datetime and end_datetime strings to datetime objects
                    start_datetime = datetime.datetime.strptime(start_datetime, '%Y-%m-%d')
                    print('try  start_datetime',start_datetime)


                    # end_datetime = datetime.datetime.strptime(end_datetime, '%Y-%m-%d %H:%M:%S')
                    end_datetime2 = datetime.datetime.strptime(end_datetime1, '%Y-%m-%d')
                    end_datetime = end_datetime2 + datetime.timedelta(days=1)
                    print('after increment end_datetime',end_datetime)

                except ValueError:
                    return JsonResponse({"error": "Invalid date format. Use 'YYYY-MM-DD HH:MM:SS' format."},
                                        status=status.HTTP_400_BAD_REQUEST)

                # Check if the user has access to the selected machine and KPI name
                try:
                    machine_data = all_Machine_data.objects.filter(machine_id__machine_id=machine_id, user_name__username=current_user,kpi__kpi_name=kpi_name)
                    print('machine_data',machine_data)
                    if not machine_data:
                        print('No data available.')
                        return JsonResponse({"status": "No data available"}, status=status.HTTP_400_BAD_REQUEST)


                except all_Machine_data.DoesNotExist:
                    return JsonResponse({"status": "Machine not found for the user"}, status=status.HTTP_400_BAD_REQUEST)

                # Fetch relevant data from Machine_KPI_Data model for the given machine_id, kpi_name, and date range
                filtered_data = Machine_KPI_Data.objects.filter(
                    machine_id=machine_id,
                    kpi_id__kpi_name=kpi_name,  # Assuming there's a field for KPI ID in the Machine_KPI_Data model
                    timestamp__range=[start_datetime, end_datetime],
                ).order_by('timestamp')
                print('filtered_data',filtered_data)

                response_data = []
                responseee = {"machine_id": machine_id,
                              "report_type": kpi_name,
                              "start_datetime": start_datetime,
                              "end_datetime": end_datetime1
                              }
                for entry in filtered_data:
                    timestamp = entry.timestamp
                    kpi_data = entry.kpi_data

                    # Extract the relevant KPI data
                    relevant_data = {"value": entry.kpi_data,"timestamp": timestamp}

                    # responseee={"machine_id": machine_id,
                    #             "report_type": kpi_name,
                    #             "start_datetime":start_datetime,
                    #             "end_datetime":end_datetime1
                    #             }



                    response_data.append(relevant_data)
                responseee["data"] = response_data
                print('responseee',responseee)

                return JsonResponse(responseee)

            else:
                return JsonResponse({"status": "login_required"})
        except Token.DoesNotExist:
            return JsonResponse({"status": "login_required"})


#
# @authentication_classes([SessionAuthentication])
# # @permission_classes([IsAuthenticated])
# class Reports_view(ViewSet):
#     @action(detail=False, method=['get'])
#     def Reports(self,request):
#         if request.user.is_authenticated:
#             # report_type = request.POST.get('report_type')
#             # machine_id = request.POST.get('machine_id')
#             # start_datetime = request.POST.get('start_datetime')
#             # end_datetime = request.POST.get('end_datetime')
#              print(',,,,,,,,,,)
#
#
#             try:
#                 request_data = json.loads(request.body)
#             except json.JSONDecodeError:
#                 return JsonResponse({"error": "Invalid JSON data."}, status=status.HTTP_400_BAD_REQUEST)
#
#             report_type = request_data.get('report_type')
#             machine_id = request_data.get('machine_id')
#             start_datetime = request_data.get('start_datetime')
#             end_datetime = request_data.get('end_datetime')
#
#             if not start_datetime or not end_datetime:
#                 return JsonResponse({"error": "start_datetime and end_datetime are required."},
#                                     status=status.HTTP_400_BAD_REQUEST)
#
#             try:
#                 # Convert the start_datetime and end_datetime strings to datetime objects
#                 start_datetime = datetime.datetime.strptime(start_datetime, '%Y-%m-%d %H:%M:%S')
#                 end_datetime = datetime.datetime.strptime(end_datetime, '%Y-%m-%d %H:%M:%S')
#             except ValueError:
#                 return Response({"error": "Invalid date format. Use 'YYYY-MM-DD HH:MM:SS' format."},
#                                 status=status.HTTP_400_BAD_REQUEST)
#
#             # Fetch the machine from Machines_List model
#             machine = Machines_List.objects.get(machine_id=machine_id)
#             Io_machine_data = IO_List.objects.filter(machine_id=machine.id).order_by('id')
#             Io_machine_data_serializer = IO_list_serializer(Io_machine_data, many=True)
#             Io_machine_data_serializer_data = Io_machine_data_serializer.data
#             print('machine',machine)
#             if not machine:
#                 return Response({"error": "Machine not found"}, status=400)
#
#             # Fetch relevant data from MachineDetails model for the given machine_id and date range
#             filtered_data = Machine_KPI_Data.objects.filter(
#                 machine_id=machine_id,
#                 timestamp__range=[start_datetime, end_datetime],
#             )
#             filtered_data_s = kpi_data_Serializer(filtered_data, many=True)
#             filtered_data_s_data = kpi_data_Serializer.data
#             # print('filtered_data_s_data',filtered_data_s_data)
#
#             plant_model_data = all_Machine_data.objects.filter(machine_id=machine.id,user_name=request.user)
#
#             print('plant_model_data_s', plant_model_data)
#
#
#             response_data = []
#             for entry in filtered_data_s_data:
#                 timestamp = entry['timestamp']
#                 machine_location = entry['machine_location']
#
#                 # Determine the relevant data based on the selected report_type
#                 # for i in range(len(Io_machine_data)):
#                 #     if Io_machine_data_serializer_data[i]['IO_type'] == "analog_input" and \
#                 #             Io_machine_data_serializer_data[i]['IO_name'] == key:
#                 if report_type in machine.analog_input:
#                     relevant_data = {report_type: entry['analog_input'][machine.analog_input.index(report_type)]}
#                 elif report_type in machine.analog_output:
#                     relevant_data = {report_type: entry['analog_output'][machine.analog_output.index(report_type)]}
#                 else:
#                     relevant_data = {}
#
#
#                 response_data.append({
#
#                     "timestamp": timestamp,
#                     "machine_id": machine_id,
#                     "machine_location": machine_location,
#                     "plant":plant_model_data[0].plant_name.plant_name,
#                     "model": plant_model_data[0].model_name.model_name,
#
#                     "data": relevant_data,
#                 })
#             print('len', len(response_data))
#
#             return JsonResponse({"data": response_data})
#         else:
#             print("else")
#             return JsonResponse({"status": "login_required"})




#
# @csrf_exempt
# @api_view(['POST'])
# @authentication_classes([SessionAuthentication])
# # @permission_classes([IsAuthenticated])
# def Reports(request):
#     if request.user.is_authenticated:
#         report_type = request.POST.get('report_type')
#         machine_id = request.POST.get('machine_id')
#         start_datetime = request.POST.get('start_datetime')
#         end_datetime = request.POST.get('end_datetime')
#
#         # try:
#         #     request_data = json.loads(request.body)
#         # except json.JSONDecodeError:
#         #     return JsonResponse({"error": "Invalid JSON data."}, status=status.HTTP_400_BAD_REQUEST)
#
#         # report_type = request_data.get('report_type')
#         # machine_id = request_data.get('machine_id')
#         # start_datetime = request_data.get('start_datetime')
#         # end_datetime = request_data.get('end_datetime')
#
#         if not start_datetime or not end_datetime:
#             return JsonResponse({"error": "start_datetime and end_datetime are required."},
#                                 status=status.HTTP_400_BAD_REQUEST)
#
#         try:
#             # Convert the start_datetime and end_datetime strings to datetime objects
#             start_datetime = datetime.strptime(start_datetime, '%Y-%m-%d %H:%M:%S')
#             end_datetime = datetime.strptime(end_datetime, '%Y-%m-%d %H:%M:%S')
#         except ValueError:
#             return Response({"error": "Invalid date format. Use 'YYYY-MM-DD HH:MM:SS' format."},
#                             status=status.HTTP_400_BAD_REQUEST)
#
#         # Fetch the machine from Machines_List model
#         machine = Machines_List.objects.filter(machine_id=machine_id).first()
#         if not machine:
#             return Response({"error": "Machine not found"}, status=400)
#
#         # Fetch relevant data from MachineDetails model for the given machine_id and date range
#         filtered_data = MachineDetails.objects.filter(
#             machine_id=machine_id,
#             timestamp__range=[start_datetime, end_datetime],
#         )
#         filtered_data_s=analog_ip_op_Serializer(filtered_data,many=True)
#         filtered_data_s_data=filtered_data_s.data
#
#         plant_model_data = all_Machine_data.objects.get(machine_id=machine_id)
#
#         print('plant_model_data_s',plant_model_data)
#
#
#         response_data = []
#         for entry in filtered_data_s_data:
#             timestamp = entry['timestamp']
#             machine_location = entry['machine_location']
#
#             # Determine the relevant data based on the selected report_type
#             if report_type in machine.analog_input:
#                 relevant_data = {report_type: entry['analog_input'][machine.analog_input.index(report_type)]}
#             elif report_type in machine.analog_output:
#                 relevant_data = {report_type: entry['analog_output'][machine.analog_output.index(report_type)]}
#             else:
#                 relevant_data = {}
#
#
#
#             response_data.append({
#
#                 'timestamp': timestamp,
#                 'machine_id': machine_id,
#                 'plant':plant_model_data.plant_name,
#                 'model':plant_model_data.model_name,
#                 'machine_location': machine_location,
#                 'data': relevant_data,
#             })
#         print('len',len(response_data))
#
#         return JsonResponse({"data": response_data})
#     else:
#         print("else")
#         return JsonResponse({"status": "login_required"})


class test(ViewSet):
    def post(self,request):
        serializer=plantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            msg=messages.success(request,'data added successfullyyyy')
            print('msg',msg)
            return Response({'message': 'success'})
        else:
            pass



    def get(self,request):

        user_data = Plant_List.objects.all()
        user_serializer = plantSerializer(user_data, many=True)
        data2=user_serializer.data

        return Response(data2)


# Machine_id :ABD2
# Start_datetime : 2023-07-19 05:31:23
# End_datetime : 2023-07-19 05:32:19
# report_type : Temperature
#
#
#
# def null_to_str(parameter1):
#     for data,vv in  parameter1.items():
#         # print('data',data)
#         # print('vv',vv)
#         # print('before',type(vv))
#
#         if vv == None:
#             parameter1[data] = str(vv)  # Convert the value to a string
#
#         # print('after',type(vv))
#         # print('vv',vv)
#
#     return parameter1


def null_to_str(data):
    if isinstance(data, list):
        return [[str(item) for item in inner_list] for inner_list in data]
    elif isinstance(data, dict):
        return {key: (str(value) if value is not None else 'None') for key, value in data.items()}
    else:
        return str(data) if data is not None else 'None'


