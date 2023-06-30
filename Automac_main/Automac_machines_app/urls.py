from django.urls import path
from . views import *


urlpatterns = [
    path('m_data', machine_data.as_view(), name='machine_data'),

]
