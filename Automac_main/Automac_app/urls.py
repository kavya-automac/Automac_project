from django.urls import path
from . views import *

from django.urls import path
# from . import views


    # Add more URL patterns as needed




urlpatterns = [

    path('dashboard/', Dashboard.as_view({'get': 'dashboard'}), name='dashboard'),
    path('machine/', Machines_view.as_view({'get': 'machine'}), name='machine'),
    path('machine_form/', Machines_view.as_view({'post': 'machine_form'}), name='machine'),
    # path('machine_details/<int:pk>/', Machines_view.as_view({'get': 'machine_details'}), name='machine_details'),
    path('machine_details/', Machines_view.as_view({'get': 'machine_details'}), name='machine_details'),
    path('reports/', Reports.as_view({'get':'reports'}), name='reports'),
    path('reportsmachine/', Reports.as_view({'get': 'reportsmachine'}), name='reportsmachine'),
    path('login/',login_view,name='login'),
    # path('username/', views.my_data_view_username, name='username'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),



]

