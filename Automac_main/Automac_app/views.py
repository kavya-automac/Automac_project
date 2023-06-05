import datetime
import json
from pathlib import Path

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.views import APIView
from django.views.generic import View
from django.db.models.signals import post_save
from django.dispatch import receiver
from . models import *
# from . serializers import *
# from.signals import *
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .serializers import *
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout



@api_view(['POST'])
@permission_classes([AllowAny])

def register(request):
    serializer = UserSerializer(data=request.data)
    print("request.data",request.data)
    print("serializer",serializer)

    # print(User.objects.get(username=request.user.username))
    if serializer.is_valid(raise_exception=True):
        print("if")

        # print(request.user, serializer.validated_data['password'], request.POST, request.GET)
        serializer.save()
        # print("serializer.data",serializer.data)
        return JsonResponse({"status":"Registered"}, status=201)

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
        user  = authenticate(username=username, password=password)
        print('authenticate_user:', user)

        if  user is not None:
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
    if 'username' in error_dict and error_dict['username'][0].code=='blank' and len(error_dict)==1:
        # print("len****",len(error_dict))
        print(error_dict['username'][0].code == 'blank')

        error_dict[new_key] = error_dict.pop('username')
        return JsonResponse({"status": error_dict["status"][0]})

    elif 'password' in error_dict and error_dict['password'][0].code=='blank' and len(error_dict)==1:
        # print("len****", len(error_dict))
        print(error_dict['password'][0].code == 'blank')
        error_dict[new_key] = error_dict.pop('password')



        return JsonResponse({"status":error_dict["status"][0]})

    elif 'username' in error_dict and error_dict['username'][0].code=='blank' and 'password' in error_dict and error_dict['password'][0].code=='blank' and len(error_dict)==2:
        # print(error_dict["status"][0])

        # print(error_dict.keys())


    #     print("sss", serializer.errors.keys())
        return JsonResponse({"status":"username_and_password_cannot_be_empty"})
    # print("sss", serializer.errors.values()[0])
    # return JsonResponse({"status":error_dict["status"][0]})
    # return JsonResponse({"status": "test"})
    # return JsonResponse({"status": error_dict["status"][0]})
    return JsonResponse({"status":"Invalid_Input"})


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


    print("loggedout",request.user.username)

    logout(request)
    return JsonResponse({"status": "Logged_out"})










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
            return  JsonResponse(data)
        else:
            print("else")
            return JsonResponse({"status":"login_required"})

@authentication_classes([SessionAuthentication])
# @permission_classes([IsAuthenticated])
class Machines_view(ViewSet):
    @action(detail=False,methods=['get'])
    def machine(self,request):
        if request.user.is_authenticated:
            print("if")
            BASE_DIR = Path(__file__).resolve().parent.parent


            print('in machines')
            machines=json.load(open(str(BASE_DIR)+"/Automac_app/machines.json"))
            return JsonResponse(machines)
        else:
            print("else")
            return JsonResponse({"status": "login_required"})

        # return redirect(Machine_Details)

    @action(detail=False, method=["get"])
    def machine_details(self, request):
        if request.user.is_authenticated:
            print("if")
            BASE_DIR = Path(__file__).resolve().parent.parent


            # current_datetime = datetime.datetime.now()
            # print("m_details")
            print("request", request.method, request.POST, request.GET)
            # print("request.method",request.GET['id'])

            if "id" in request.GET and "module" in request.GET:
                module = request.GET["module"]

                # @action(detail=False, method=["get"])
                # def documents(self, request):
                #     fields = [
                #         {
                #
                #         }
                #     ]
                if module == "Details":
                    # file
                    data = json.load(open(str(BASE_DIR)+"/Automac_app/machine_details.json"))

                elif module == "kpis":
                    data = json.load(open(str(BASE_DIR)+"/Automac_app/machine_details(kpis).json"))

                elif module == "iostatus":
                    data = json.load(open(str(BASE_DIR)+"/Automac_app/machine_details(io_status).json"))
                else:
                    data = {
                        'status': 'please_enter_correct_module_name'
                    }
            else:
                data = {
                    'status': 'enter_correct_id_and_module'
                }

                # @action(detail=False, method=["get"])
                # def documents(self, request):
                #     fields = [
                #         {
                #
                #         }
                #     ]
                #
                # @action(detail=False, method=["get"])
                # def Techinacal_details(self, request):
                #     details = [
                #         {
                #
                #         }
                #     ]

            return JsonResponse(data)
        else:
            return JsonResponse({"status":"login_required"})






@authentication_classes([SessionAuthentication])
# @permission_classes([IsAuthenticated])
class Reports(ViewSet):
    @action(detail=False, method=['get'])


    def reports(self,request):
        if request.user.is_authenticated:
            print("if")

            BASE_DIR = Path(__file__).resolve().parent.parent

            data= json.load(open(str(BASE_DIR)+"/Automac_app/reports.json"))
            return JsonResponse(data)
        else:
            print("else")
            return JsonResponse({"status":"login_required"})


    @action(detail=False, method=['get'])
    def reportsmachine(self, request):
        if request.user.is_authenticated:
            print("if")
            BASE_DIR = Path(__file__).resolve().parent.parent

            # machine_data = json.load(open(str(BASE_DIR)+"/Automac_app/machines.json"))
            # print('request',request.method,request.GET)
            # data = json.load(open("figmaapp/reports_selectmachine.json"))
            # print(data["Result"][0]["machine_id"])
            # print("id",machine_data["machines"][0]["id"])
            # print("id", machine_data["machines"][1]["id"])
            # print(machine_data["machines"])
            # print(type(machine_data["machines"]))
            # for i in range(1,len(machine_data["machines"])):
            # print("len",len(machine_data["machines"]))
            if  'id' in request.GET:
                # for i in range(len(machine_data["machines"])):
                #     if request.GET['id'] == machine_data["machines"][i]["id"]:
                #         print(request.GET['id'])
                #         print(machine_data["machines"][i]["id"])
                data = json.load(open(str(BASE_DIR)+"/Automac_app/machines.json"))
            else:
                data={"status":"enter_id"}

            return JsonResponse(data)

        else:
            print("else")
            return JsonResponse({"status":"login_required"})


# Build paths inside the project like this: BASE_DIR / 'subdir'.


















# class Machine_detail(ViewSet):
#     @action(detail=False,method=["get"])
#     def m_details(self,request):
#
#         current_datetime = datetime.datetime.now()
#         # print("m_details")
#         print("request",request.method,request.POST, request.GET)
#         # print("request.method",request.GET['id'])
#
#
#         if 'id' in  request.GET and 'module' in request.GET:
#             module = request.GET["module"]
#             if module=="Details":
#                 # file
#                 data=json.load(open("figma_app/machine_details.json"))
#
#             elif module == "kpis":
#                 data=json.load(open("figma_app/machine_details(kpis).json"))
#
#             elif module == "iostatus":
#                  data =json.load(open("figma_app/machine_details(io_status).json"))
#             else:
#                 data = {
#                     'response':'please enter correct module name'
#                 }
#         else:
#             data = {
#                 'response': 'enter correct id and module'
#             }
#
#             # @action(detail=False, method=["get"])
#             # def documents(self, request):
#             #     fields = [
#             #         {
#             #
#             #         }
#             #     ]
#             #
#             # @action(detail=False, method=["get"])
#             # def Techinacal_details(self, request):
#             #     details = [
#             #         {
#             #
#             #         }
#             #     ]
#
#
#
#         return JsonResponse(data)













# class Machine_Details(ViewSet):
#     @action(detail=False, methods=['get'])
#     def details(self, request):
#         current_datetime = datetime.datetime.now()
#
#         particular_machine_detail={
#             'id': 1,
#             'name': 'Machine 1',
#         }
#         data = [
#             {
#             'id':'1',
#             'machine_name':'machine1',
#             'model':'white',
#             'Date_of_installation':'2020 Spring',
#             'Detail 1':2770,
#             'Detail 2':79.00
#            },
#         {
#             # date_only = current_datetime.strftime("%Y-%m-%d")
#
#             'Manuals and docs':[{'name':'Electrical Drawing','posted_by':'harsha','time':current_datetime},
#                 {'name':'VFD Datasheet','posted_by':'harsha','time':current_datetime}]
#             },
#         {
#             'Techincal Details':{'date':current_datetime.strftime("%Y-%m-%d"),'number':'05822-XSP','Make':'Delta','Code':'DS120R'}
#
#             }
#         ]
#
#         return Response(data)
#
#     @action(detail=False, methods=['get'])
#     def kpis(self, request):
#         data = [
#             {
#                 'label':'New Products',
#                 'value':540,
#                 'units':'ltr'},
#             {
#
#             },
#             {
#                 'temperature': 25,
#                 'humidity': 50}
#                 # Add other KPI fields here
#
#             # Add more KPI data dictionaries as needed
#         ]
#         return Response(data)
#
#     @action(detail=False, methods=['get'])
#     def iostatus(self, request):
#         data = {
#             'digital': [{
#                 'sensor_name':'sensor name1',
#                 'input': 'input',
#                 'value':'On'
#                 },
#             {
#                 'sensor_name':'sensor name1',
#                 'output': 'output',
#                 'value':'On'
#             },
#                 {
#                 'sensor_name':'sensor name2',
#                 'input': 'input',
#                 'value':'Off'
#                 },
#             {
#                 'sensor_name':'sensor name2',
#                 'output': 'output',
#                 'value':'On'
#             }
#             ],
#             'analog': [
#                 {
#                     'sensor_name': 'sensor name1',
#                     'input': 'input',
#                     'value': '250 ',
#                     'units': 'rmp',
#                 },
#                 {
#                     'sensor_name': 'sensor name1',
#                     'output': 'output',
#                     'value': '250 ',
#                     'units': 'rmp',
#                 },
#                 ]
#         }
#         return Response(data)






