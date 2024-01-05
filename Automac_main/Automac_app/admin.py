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
    # list_display = ['id','kpi_name','kpi_data','kpi_unit']
    list_display = ['id','kpi_name','kpi_inventory_id','data_points']

@admin.register(Kpi_Inventory)
class Kpi_Inventory_ListAdmin(admin.ModelAdmin):
    # list_display = ['id','kpi_name','kpi_data','kpi_unit']
    list_display = ['id','Kpi_Type','labels']



@admin.register(Machines_List)
class Machines_ListAdmin(admin.ModelAdmin):
    list_display = ['machine_id','machine_image','machine_name',
                    'machine_location','date_of_installation','machine_state']





@admin.register(Company_List)
class Company_ListAdmin(admin.ModelAdmin):
    list_display = ['id','company_name','company_location','company_logo']

@admin.register(all_Machine_data)
class all_Machine_dataAdmin(admin.ModelAdmin):
    list_display = ['id','user_name','company_name','plant_name','machine_id','model_name','kpi']
    search_fields =all_Machine_data.SearchableFields
# admin.site.register(all_Machine_data)




@admin.register(IO_List)
class all_Machine_dataAdmin(admin.ModelAdmin):
    list_display = ['machine_id','IO_type','IO_name','IO_value','IO_color','IO_Unit','Control']
