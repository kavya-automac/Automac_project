from django.urls import path
from . views import *

from django.urls import path
# from . import views
from django.views.decorators.csrf import csrf_exempt


    # Add more URL patterns as needed


from . import views

urlpatterns = [

    path('dashboard/', Dashboard.as_view({'get': 'dashboard'}), name='dashboard'),
    # path('machine/', MachinesView.as_view({'get': 'machine'}), name='machine'),
    path('machine_list/', MachinesView.as_view({'get': 'machine_list'}), name='machine'),
    # path('machine_details/<int:pk>/', MachinesView.as_view({'get': 'machine_details'}), name='machine_details'),
    path('machine_details/', MachinesView.as_view({'get': 'machine_details'}), name='machine_details'),
    # path('machine_details/', MachinesView.as_view({'get': 'machine_details','post': 'machine_details'}), name='machine_details'),
    path('Trail_details/', Trails.as_view({'get': 'Trail_details'}), name='Trail_details'),
    path('Trail_List/', Trails.as_view({'get': 'Trail_List'}), name='Trail_List'),
    path('login/',login_view,name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    # path('Reports/', Reports_view.as_view({'get':'Reports'}), name='Reports'),
    path('Reports/', ReportsView.as_view({'get': 'Reports'}), name='Reports'),
    path('Report_List/', ReportsView.as_view({'get': 'Report_List'}), name='Report_List'),
    path('test/', test.as_view({'get': 'get'}), name='test'),
    path('test_post/', test.as_view({'post': 'post'}), name='test'),
    path('machine_control/', views.machine_control),

]