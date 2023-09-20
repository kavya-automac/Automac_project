from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from.serializers import *
from . models import *

from Automac_app.models import Machines_List
from Automac_app.serializers import usermachineSerializer

# from Automac_app import  calculations



# from models import *
#
# machines_list_data = Machines_List.objects.all()
# # machine_details_data = Automac_machines_app.models.get_MachineDetails()
# print('machines_list_data',machines_list_data)
#
#



class machine_data(APIView):
    # def post(self,request):
    #     serializer=ABCSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({'message':'success'})
    def get(self,request):

        user_data = Machines_List.objects.all()
        user_serializer = usermachineSerializer(user_data, many=True)
        data2=user_serializer.data
        info = calculations.kpi_data_to_database()
        print('infoooooooooooooooooooooooooooo',info)

        return Response(data2)


class users_data(APIView):
    def get(self, request):
        data = Machines_List.objects.all()
        serializer = usermachineSerializer(data, many=True)

        print('data',serializer.data)

        return Response(serializer.data)