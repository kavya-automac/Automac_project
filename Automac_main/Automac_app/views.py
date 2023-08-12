from datetime import datetime
from pathlib import Path
# from django.contrib.auth.decorators import login_required
# from django.http import JsonResponse
# from django.shortcuts import render, redirect
# from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
# from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
# from rest_framework.views import APIView
# from django.views.generic import View
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from . models import *
# from . serializers import *
# from.signals import *
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
# from rest_framework.response import Response
from .serializers import *
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.apps import apps
from . history import history_fun
from Automac_machines_app.serializers import machineSerializer,analog_ip_op_Serializer,machineSerializer_two,analog_ip_op_Serializer
# from Automac_machines_app.serializers import *
from Automac_machines_app.models import MachineDetails

# from .Automac_machines_app.models import MachineDetails


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
            login(request, user)
            print("logged in:", request.user.username)
            return JsonResponse({"status": "user_validated"})

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
@api_view(['GET'])
# @authentication_classes([SessionAuthentication])
# @permission_classes([IsAuthenticated])
def logout_view(request):
    print("entering logout")
    print("loggedout", request.user.username)

    logout(request)
    return JsonResponse({"status": "Logged_out"})

#convert list or dict values into string


@authentication_classes([SessionAuthentication])
# @permission_classes([IsAuthenticated])
# @login_required(login_url='login_view')
class Dashboard(ViewSet):
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        if request.user.is_authenticated:
            print("if")
            BASE_DIR = Path(__file__).resolve().parent.parent
            print('BASE_DIR', type(BASE_DIR))

            data = json.load(open(str(BASE_DIR)+"/Automac_app/dashboard.json"))
            return JsonResponse(data)
        else:
            print("else")
            return JsonResponse({"status": "login_required"})


@authentication_classes([SessionAuthentication])
# @permission_classes([IsAuthenticated])
class MachinesView(ViewSet):
    @action(detail=False, methods=['get'])
    def machine_list(self, request):
        if request.user.is_authenticated:
            print('userssss', request.user)
            get_user_data= all_Machine_data.objects.filter(user_name=request.user)
            # print('get_user_data',get_user_data[0].company_name.company_name)
            get_user_data_s= all_Machine_data_Serializer2(get_user_data,many=True)
            get_user_data_s_data= get_user_data_s.data

            print('get_user_data_s_data',get_user_data_s_data)
            for i in range(0,len(get_user_data_s_data)):
                get_user_data_s_data[i].update(company_name=get_user_data[i].company_name.company_name)
                get_user_data_s_data[i].update(plant_name=get_user_data[i].plant_name.plant_name)
                get_user_data_s_data[i].update(model_name=get_user_data[i].model_name.model_name)
                get_user_data_s_data[i].update(machine_id=get_user_data[i].machine_id.machine_name)
                # get_user_data_s_data[i].update(machine_id=get_user_data[i].machine_id.machine_location)
                get_user_data_s_data[i].update(line_name=str(get_user_data[i].line_name))
            print('get_user_data_s_data',get_user_data_s_data)



            return JsonResponse({"machine_list": get_user_data_s_data})

            # form_fun = forms_data()
        else:
            print("else")
            return JsonResponse({"status": "login_required"})

    @action(detail=False, method=["get"])
    def machine_details(self, request):
        if request.user.is_authenticated:
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
                    # print('general_serialzer_data_1',general_serialzer_data_1)

                    plant_line_data=all_Machine_data.objects.filter(machine_id=general_data.id,user_name=request.user)
                    # print('plant_line_data',plant_line_data)

                    if not plant_line_data.exists():
                        # If the plant_line_data is empty, return a response indicating that the user doesn't have access.
                        return JsonResponse({"message": "User does not have access to this machine."}, status=403)


                    s_data=all_Machine_data_Serializer(plant_line_data,many=True)
                    s_data_d=s_data.data
                    print('plant_line_data',plant_line_data[0].plant_name,type(plant_line_data))
                    for f_names in range(0,len(plant_line_data)):
                        s_data_d[f_names].update(plant_name=plant_line_data[f_names].plant_name.plant_name)
                        s_data_d[f_names].update(model_name=plant_line_data[f_names].model_name.model_name)
                        s_data_d[f_names].update(line_name=str(plant_line_data[f_names].line_name))
                        print('s_data',s_data_d)
                        general_serialzer_data_1.update(dict(s_data_d[0]))
                        # general_serialzer_data_1=dict(s_data_d)
                    if not s_data_d:
                        return JsonResponse({"general_data": general_serialzer_data_1})

                    Manuals_and_Docs=[{"Document_name":"Electrical_Drawing",
                                       "Uploaded_by":"harsha",
                                       "Date":"27/07/2023",
                                       "Url":"http://127.0.0.1:8000/media/images/KRESUME.png"}]
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

                    data = json.load(open(str(BASE_DIR)+"/Automac_app/machine_details(kpis).json"))
                elif module == "iostatus":
                    try:
                        io_data = Machines_List.objects.get(machine_id=machine_id)
                    except Machines_List.DoesNotExist:
                        error_message = "Please enter a valid machine_id."
                        return JsonResponse({"error": error_message}, status=400)  # Return an error response

                    # io_data = Machines_List.objects.get(machine_id=machine_id)
                    print('io_data',io_data.machine_id)

                    io_serializer = IostatusmachineSerializer(io_data)
                    io_serializer_data = io_serializer.data
                    print('io_serializer_data', io_serializer_data)
                    # print('issssssssssssssssss',io_serializer_data.db_timestamp)


                    machine_values_data = MachineDetails.objects.filter(machine_id=io_data.machine_id).order_by('-timestamp').first()
                    print('machine_values_data', machine_values_data)

                    # last_valies_data = machineSerializer(machine_values_data).data if machine_values_data else {}
                    last_valies_data_1 = machineSerializer(machine_values_data)
                    last_valies_data=last_valies_data_1.data
                    # print('last_valies_data',machine_values_data.db_timestamp)
                    print('last_valies_data',last_valies_data)

                    # for i in range(len(io_serializer_data)):
                    #     print('i', i)
                    io_data = io_serializer_data
                    print('lllllllllllllllll',io_data)
                    io_data['db_timestamp'] = str(last_valies_data.get('timestamp'))
                    # io_data['db_timestamp'] = last_valies_data.get('timestamp', str(None))
                    # io_data['db_timestamp'] = machine_values_data.db_timestamp
                    # Create a new list of dictionaries with the desired format for digital_input
                    # ###### digital_input
                    digital_input_data = []
                    for key, value in zip(io_data['digital_input'], last_valies_data.get('digital_input', [])):
                        value_str = "On" if value else "Off"  # Convert boolean to "On" or "Off"

                        digital_input_data.append({"name": key, "value": value_str})
                    print('digital_input_data',digital_input_data)
                    io_data['digital_input'] = digital_input_data

                    # ###### digital_output

                    digital_output_data = []
                    for key, value in zip(io_data['digital_output'], last_valies_data.get('digital_output', [])):
                        value_str = "On" if value else "Off"  # Convert boolean to "On" or "Off"

                        digital_output_data.append({"name": key, "value": value_str})
                    print('digital_output_data', digital_output_data)
                    io_data['digital_output'] = digital_output_data

                    # ###### analog_input

                    analog_input_data = []
                    for key, value in zip(io_data['analog_input'], last_valies_data.get('analog_input', [])):
                        analog_input_data.append({"name": key, "value": str(value)})
                    print('analog_input_data', analog_input_data)
                    io_data['analog_input'] = analog_input_data

                    # ###### analog_output

                    analog_output_data = []
                    for key, value in zip(io_data['analog_output'], last_valies_data.get('analog_output', [])):
                        analog_output_data.append({"name": key, "value": str(value)})
                    print('analog_input_data', analog_output_data)
                    io_data['analog_output'] = analog_output_data
                # print('llllllllllllll',io_data)


                    data = {'iostatus': io_serializer_data}

                    # for i in range(len(io_serializer_data)):
                    #     print('i', i)
                    #     io_serializer_data[i]['db_timestamp'] = last_valies_data.get('db_timestamp', None)
                    #
                    #     di = dict(zip(io_serializer_data[i]['digital_input'], last_valies_data.get('digital_input', [])))
                    #     print('di',di)
                    #     print(' last_valies_data.get', last_valies_data.get('digital_input', []))
                    #     name=io_serializer_data[i]['digital_output']
                    #     value= last_valies_data.get('digital_output', [])
                    #
                    #     do = dict(zip(io_serializer_data[i]['digital_output'], last_valies_data.get('digital_output', [])))
                    #     ai = dict(zip(io_serializer_data[i]['analog_input'], last_valies_data.get('analog_input', [])))
                    #     ao = dict(zip(io_serializer_data[i]['analog_output'], last_valies_data.get('analog_output', [])))
                    #
                    #     io_serializer_data[i]['digital_input'] = di
                    #     io_serializer_data[i]['digital_output'] = do
                    #     io_serializer_data[i]['analog_input'] = ai
                    #     io_serializer_data[i]['analog_output'] = ao
                    #
                    # data = {'iostatus': io_serializer_data}

                    # data = json.load(open(str(BASE_DIR)+"/Automac_app/machine_details(io_status).json"))
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




def testing_sessions(request):
    if request.user.is_authenticated:
        session_key = request.session.session_key
        print("Session Key:", session_key)

        request.session['dummy_data'] = 'Hello, World!'
        json_data_1=json.dumps({"name":"kavya","company":"Automac"})
        request.session['json_data'] =json_data_1
        # messages.success(request, 'Dummy data successfully stored in session.')
        dummy = request.session.get('dummy_data')
        json_data = request.session.get('json_data')
        print("Dummy Data:", dummy)
        print("json data:", json_data)

        # messages.warning(request, 'warning.')

    else:
        pass

@authentication_classes([SessionAuthentication])
# @permission_classes([IsAuthenticated])
class Trails(ViewSet):
    @action(detail=False, method=['get'])
    def Trail_details(self,request):
        if request.user.is_authenticated:
            print("if")
            data_session=testing_sessions(request)
            # print('data_session',data_session)

            machine_id = request.GET.get('machine_id')
            date = request.GET.get('date')
            # end_datetime = request.GET.get('end_datetime')
            print('request',request.method,request.GET)

            trail_detail_data = history_fun(machine_id,date)
            # reports_data = history_fun(machine_id,start_datetime,end_datetime)
            return trail_detail_data

        else:
            print("else")
            return JsonResponse({"status": "login_required"})



    @action(detail=False, method=['get'])
    def Trail_List(self, request):
        if request.user.is_authenticated:
            print("if")

            BASE_DIR = Path(__file__).resolve().parent.parent
            get_user_data = all_Machine_data.objects.filter(user_name=request.user)
            # print('get_user_data',get_user_data[0].company_name.company_name)
            get_user_data_s = all_Machine_data_Serializer2(get_user_data, many=True)
            get_user_data_s_data = get_user_data_s.data

            print('get_user_data_s_data', get_user_data_s_data)
            for i in range(0, len(get_user_data_s_data)):
                get_user_data_s_data[i].update(company_name=get_user_data[i].company_name.company_name)
                get_user_data_s_data[i].update(plant_name=get_user_data[i].plant_name.plant_name)
                get_user_data_s_data[i].update(model_name=get_user_data[i].model_name.model_name)
                get_user_data_s_data[i].update(machine_id=get_user_data[i].machine_id.machine_name)
                # get_user_data_s_data[i].update(machine_id=get_user_data[i].machine_id.machine_location)
                get_user_data_s_data[i].update(line_name=str(get_user_data[i].line_name))
            print('get_user_data_s_data', get_user_data_s_data)

            return JsonResponse({"Trail_list": get_user_data_s_data})



        else:
            print("else")
            return JsonResponse({"status":"login_required"})




@authentication_classes([SessionAuthentication])
# @permission_classes([IsAuthenticated])
class Reports_view(ViewSet):
    @action(detail=False, method=['get'])
    def Reports(self,request):
        if request.user.is_authenticated:
            # report_type = request.POST.get('report_type')
            # machine_id = request.POST.get('machine_id')
            # start_datetime = request.POST.get('start_datetime')
            # end_datetime = request.POST.get('end_datetime')


            try:
                request_data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON data."}, status=status.HTTP_400_BAD_REQUEST)

            report_type = request_data.get('report_type')
            machine_id = request_data.get('machine_id')
            start_datetime = request_data.get('start_datetime')
            end_datetime = request_data.get('end_datetime')

            if not start_datetime or not end_datetime:
                return JsonResponse({"error": "start_datetime and end_datetime are required."},
                                    status=status.HTTP_400_BAD_REQUEST)

            try:
                # Convert the start_datetime and end_datetime strings to datetime objects
                start_datetime = datetime.strptime(start_datetime, '%Y-%m-%d %H:%M:%S')
                end_datetime = datetime.strptime(end_datetime, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                return Response({"error": "Invalid date format. Use 'YYYY-MM-DD HH:MM:SS' format."},
                                status=status.HTTP_400_BAD_REQUEST)

            # Fetch the machine from Machines_List model
            machine = Machines_List.objects.get(machine_id=machine_id)
            print('machine',machine)
            if not machine:
                return Response({"error": "Machine not found"}, status=400)

            # Fetch relevant data from MachineDetails model for the given machine_id and date range
            filtered_data = MachineDetails.objects.filter(
                machine_id=machine_id,
                timestamp__range=[start_datetime, end_datetime],
            )
            filtered_data_s = analog_ip_op_Serializer(filtered_data, many=True)
            filtered_data_s_data = filtered_data_s.data
            # print('filtered_data_s_data',filtered_data_s_data)

            plant_model_data = all_Machine_data.objects.filter(machine_id=machine.id,user_name=request.user)

            print('plant_model_data_s', plant_model_data)


            response_data = []
            for entry in filtered_data_s_data:
                timestamp = entry['timestamp']
                machine_location = entry['machine_location']

                # Determine the relevant data based on the selected report_type
                if report_type in machine.analog_input:
                    relevant_data = {report_type: entry['analog_input'][machine.analog_input.index(report_type)]}
                elif report_type in machine.analog_output:
                    relevant_data = {report_type: entry['analog_output'][machine.analog_output.index(report_type)]}
                else:
                    relevant_data = {}


                response_data.append({

                    "timestamp": timestamp,
                    "machine_id": machine_id,
                    "machine_location": machine_location,
                    "plant":plant_model_data[0].plant_name.plant_name,
                    "model": plant_model_data[0].model_name.model_name,

                    "data": relevant_data,
                })
            print('len', len(response_data))

            return JsonResponse({"data": response_data})
        else:
            print("else")
            return JsonResponse({"status": "login_required"})

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


