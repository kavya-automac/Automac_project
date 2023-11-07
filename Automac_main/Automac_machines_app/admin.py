from django.contrib import admin

# Register your models here.
from .models import *

# admin.site.register(MachineDetails)
# admin.site.register(Machine_KPI_Data)


@admin.register(MachineDetails)
class all_Machine_dataAdmin(admin.ModelAdmin):
    list_display = ['id','db_timestamp','timestamp','machine_id','digital_input','digital_output','analog_input','analog_output','other']
    search_fields =MachineDetails.SearchableFields

@admin.register(Machine_KPI_Data)
class all_Machine_dataAdmin(admin.ModelAdmin):
    list_display=['id','machine_id','kpi_id','kpi_data','timestamp']
    search_fields =Machine_KPI_Data.SearchableFields
