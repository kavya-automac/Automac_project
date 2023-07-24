from django.urls import path
from . views import *

from django.urls import path
# from . import views


    # Add more URL patterns as needed




urlpatterns = [

    path('dashboard/', Dashboard.as_view({'get': 'dashboard'}), name='dashboard'),
    # path('machine/', MachinesView.as_view({'get': 'machine'}), name='machine'),
    path('machine_form/', MachinesView.as_view({'get': 'machine_form'}), name='machine'),
    # path('machine_details/<int:pk>/', MachinesView.as_view({'get': 'machine_details'}), name='machine_details'),
    path('machine_details/', MachinesView.as_view({'get': 'machine_details'}), name='machine_details'),
    path('Trail_details/', Trails.as_view({'get': 'Trail_details'}), name='Trail_details'),
    path('Trail_machine/', Trails.as_view({'get': 'Trail_machine'}), name='Trail_machine'),
    path('login/',login_view,name='login'),
    # path('username/', views.my_data_view_username, name='username'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('test/', test.as_view({'get': 'get'}), name='test'),
    path('test_post/', test.as_view({'post': 'post'}), name='test'),

]

# for query_data in query:
#     if query_data == 'company':
#         company_data = Company_List.objects.all()
#         company_data_serializer = companySerializer(company_data, many=True)
#         serialized_company_data = company_data_serializer.data
#
#         # company_names = []
#         for i in range(0, len(company_data)):
#             c_data = serialized_company_data[i]['company_name']
#             print('data1', c_data)
#             form_values.append(c_data)
#
#
#     elif query_data =="plant":
#         plant_data = Plant_List.objects.all()
#         plant_data_serializer = plantSerializer(plant_data, many=True)
#         serialized_plant_data = plant_data_serializer.data
#         for i in range(0, len(plant_data)):
#             p_data = serialized_plant_data[i]['plant_name']
#             print('data2', p_data)
#             p_names=p_data['plant_name']
#
#             form_values[p_names]=p_data
#         print('palnt',form_values)
#
#     elif query_data == "line":
#
#         line_data = Line_List.objects.all()
#         line_data_serializer = companySerializer(line_data, many=True)
#         serialized_line_data = line_data_serializer.data
#         for i in range(0, len(line_data)):
#             l_data = serialized_line_data[i]['line_name']
#             print('data3', l_data)
#             form_values.append(l_data)
#     elif query_data == "model":
#         model_data = Model_List.objects.all()
#         model_data_serializer = modelSerializer(model_data, many=True)
#         serialized_model_data = model_data_serializer.data
#         for i in range(0, len(model_data)):
#             data5 = serialized_model_data[i]['model_name']
#             print('data5', data5)
#             form_values.append(data5)
#
#
#     elif query_data == "machine":
#         machine_data = Machines_List.objects.all()
#         machine_data_serializer = usermachineSerializer(machine_data, many=True)
#         serialized_machine_data = machine_data_serializer.data
#         for i in range(0, len(machine_data)):
#             m_data = serialized_machine_data[i]['machine_name']
#             print('data4', m_data)
#             form_values.append(m_data)
#     print('form_values',form_values)

