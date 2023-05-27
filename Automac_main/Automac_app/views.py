import datetime
import json

from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.views.generic import View
from django.db.models.signals import post_save
from django.dispatch import receiver
from . models import *
# from . serializers import *
# from.signals import *
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet


class Dashboard(ViewSet):
    @action(detail=False, methods=['get'])

    def dashboard(self, request):

        data = json.load(open("Automac_app/dashboard.json"))
        return  JsonResponse(data)

class Machines_view(ViewSet):
    @action(detail=False,methods=['get'])
    def machine(self,request):
        print('in manchines')
        machines=json.load(open("Automac_app/machines.json"))
        return JsonResponse(machines)
        # return redirect(Machine_Details)

    @action(detail=False, method=["get"])
    def machine_details(self, request):

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
                data = json.load(open("Automac_app/machine_details.json"))

            elif module == "kpis":
                data = json.load(open("Automac_app/machine_details(kpis).json"))

            elif module == "iostatus":
                data = json.load(open("Automac_app/machine_details(io_status).json"))
            else:
                data = {
                    'response': 'please enter correct module name'
                }
        else:
            data = {
                'response': 'enter correct id and module'
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







class Reports(ViewSet):
    @action(detail=False, method=['get'])
    def reports(self,request):
        data= json.load(open("Automac_app/reports.json"))
        return JsonResponse(data)

    @action(detail=False, method=['get'])
    def reportsmachine(self, request):
        machine_data = json.load(open("Automac_app/machines.json"))
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
            data = json.load(open("Automac_app/machines.json"))
        else:
            data={"msg":"enter machine id"}

        return JsonResponse(data)






















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






