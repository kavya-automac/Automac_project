from django.urls import path
from . views import *

from django.urls import path
# from . import views
from django.views.decorators.csrf import csrf_exempt


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
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('Reports/', Reports, name='Reports'),
    # path('Reports/', csrf_exempt(Reports_view.as_view({'post': 'Reports'})), name='Reports'),

    path('test/', test.as_view({'get': 'get'}), name='test'),
    path('test_post/', test.as_view({'post': 'post'}), name='test'),

]