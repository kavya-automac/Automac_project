from django.urls import path
from . views import *

from django.urls import path
from .views import Dashboard


    # Add more URL patterns as needed




urlpatterns = [

    path('dashboard/', Dashboard.as_view({'get': 'dashboard'}), name='dashboard'),
    path('machine/', Machines_view.as_view({'get': 'machine'}), name='machine'),
    path('machine_details/', Machines_view.as_view({'get': 'machine_details'}), name='machine_details'),
    path('reports/', Reports.as_view({'get':'reports'}), name='reports'),
    path('reportsmachine/', Reports.as_view({'get': 'reportsmachine'}), name='reportsmachine'),



]

