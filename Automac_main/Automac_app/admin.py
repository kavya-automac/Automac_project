from django.contrib import admin

from .models import *



# admin.site.register(Model_List)
# admin.site.register(Plant_List)
# admin.site.register(Machine_Kpi_List)
# admin.site.register(Machines_List)



@admin.register(Line_List)
class Line_ListAdmin(admin.ModelAdmin):
    list_display = ['id','line_name']

@admin.register(Model_List)
class Model_ListAdmin(admin.ModelAdmin):
    list_display = ['id','model_name']

@admin.register(Plant_List)
class Plant_ListAdmin(admin.ModelAdmin):
    list_display = ['id','plant_name','plant_location']

@admin.register(Machine_Kpi_List)
class Machine_Kpi_ListAdmin(admin.ModelAdmin):
    list_display = ['id','kpi_name','kpi_data','kpi_unit']

@admin.register(Machines_List)
class Machines_ListAdmin(admin.ModelAdmin):
    list_display = ['machine_id','machine_image','machine_name',
                    'machine_location','digital_input','digital_output','analog_input',
                    'analog_output','date_of_installation','machine_state']





@admin.register(Company_List)
class Company_ListAdmin(admin.ModelAdmin):
    list_display = ['id','company_name','company_location']

@admin.register(all_Machine_data)
class all_Machine_dataAdmin(admin.ModelAdmin):
    list_display = ['id','user_name','company_name','plant_name','machine_id','model_name']

# admin.site.register(all_Machine_data)

