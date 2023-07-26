from django.contrib import admin

from .models import *



admin.site.register([Line_List,Model_List,Plant_List,Machine_Kpi_List,Machines_List,Company_List,all_Machine_data])
# admin.site.register(Model_List)
# admin.site.register(Plant_List)
# admin.site.register(Machine_Kpi_List)
# admin.site.register(Machines_List)
