from pathlib import Path
# from django.contrib.auth.decorators import login_required
# from django.http import JsonResponse
# from django.shortcuts import render, redirect
# from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
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
from Automac_machines_app.serializers import machineSerializer
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


machine_data = Machines_List.objects.all()
machine_data_serializer = usermachineSerializer(machine_data, many=True)
serialized_machine_data = machine_data_serializer.data
# print('serialized_machine_data', serialized_machine_data)

plant_data = Plant_List.objects.all()
plant_data_serializer = plantSerializer(plant_data, many=True)
serialized_plant_data = plant_data_serializer.data
# print('serialized_plant_data', serialized_plant_data)

model_data = Model_List.objects.all()
model_data_serializer = modelSerializer(model_data, many=True)
serialized_model_data = model_data_serializer.data
# print('serialized_model_data', serialized_model_data)

company_data = Company_List.objects.all()
company_data_serializer = companySerializer(company_data, many=True)
serialized_company_data = company_data_serializer.data

line_data = Line_List.objects.all()
line_data_serializer = companySerializer(line_data, many=True)
serialized_line_data = line_data_serializer.data

company_names = []
for i in range(0, len(company_data)):
    c_data = serialized_company_data[i]['company_name']
    # print('data1', c_data)
    company_names.append(c_data)

plant_names = []
for i in range(0, len(plant_data)):
    p_data = serialized_plant_data[i]['plant_name']
    # print('data2', p_data)
    plant_names.append(p_data)

line_names = []
for i in range(0, len(line_data)):
    l_data = serialized_line_data[i]['line_name']
    # print('data3', l_data)
    line_names.append(l_data)

machines_name = []
for i in range(0, len(machine_data)):
    m_data = serialized_machine_data[i]['machine_name']
    # print('data4', m_data)
    machines_name.append(m_data)

print('machines_name', machines_name)

model_names = []
for i in range(0, len(model_data)):
    data5 = serialized_model_data[i]['model_name']
    # print('data5', data5)
    model_names.append(data5)





def forms_data():
    data = {'company': company_names, 'plant': plant_names, 'line': line_names, 'model': model_names,
            'machine': machines_name}

    query = ['line', 'model', 'machine']
    # query = ['machine']
    # print(data['c'])

    form_values = []

    for item in query:
        form_values.append(data[item])

    resultant_form_values = dict(zip(query, form_values))
    print(resultant_form_values)
    return resultant_form_values


@authentication_classes([SessionAuthentication])
# @permission_classes([IsAuthenticated])
class MachinesView(ViewSet):
    @action(detail=False, methods=['get'])
    def machine_form(self, request):
        if request.user.is_authenticated:
            form_fun = forms_data()
            return JsonResponse(form_fun)
        else:
            print("else")
            return JsonResponse({"status": "login_required"})

    @action(detail=False, method=["get"])
    def machine_details(self, request):
        if request.user.is_authenticated:
            print("if")
            BASE_DIR = Path(__file__).resolve().parent.parent

            id=request.query_params.get('id')
            d=Machines_List.objects.filter(id=id)

            print("request", request.method, request.POST, request.GET)
            # print("request.method",request.GET['id'])
            # q=Machines_List.objects.filter(id=id).values('id','machine_name','machine_location','date_of_installation')
            # print('q',q)

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
                    # id = request.query_params.get('id')
                    general_data = Machines_List.objects.filter(id=id)
                    general_serialzer=generalmachineSerializer(general_data,many=True)
                    general_serialzer_data=general_serialzer.data
                    print('general_serialzer_data',general_serialzer_data)
                    data = {'general_details':general_serialzer_data}
                    # data = json.load(open(str(BASE_DIR)+"/Automac_app/machine_details.json"))

                elif module == "kpis":

                    data = json.load(open(str(BASE_DIR)+"/Automac_app/machine_details(kpis).json"))

                elif module == "iostatus":
                    io_data = Machines_List.objects.filter(id=id)
                    io_serializer=IostatusmachineSerializer(io_data,many=True)
                    io_serializer_data=io_serializer.data
                    # print('kpi_serializer_data',io_serializer_data)
                    print('io_serializer_data',io_serializer_data)

                    data={'iostatus':io_serializer_data}
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
            return JsonResponse({"history": trail_detail_data})

        else:
            print("else")
            return JsonResponse({"status": "login_required"})



    @action(detail=False, method=['get'])
    def Trail_machine(self, request):
        if request.user.is_authenticated:
            print("if")

            BASE_DIR = Path(__file__).resolve().parent.parent


            if  'id' in request.GET:

                data = json.load(open(str(BASE_DIR)+"/Automac_app/machines.json"))
            else:
                data={"status":"enter_id"}

            return JsonResponse(data)

        else:
            print("else")
            return JsonResponse({"status":"login_required"})


# Build paths inside the project like this: BASE_DIR / 'subdir'.




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
