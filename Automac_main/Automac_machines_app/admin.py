from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(MachineDetails)
admin.site.register(Machine_KPI_Data)
