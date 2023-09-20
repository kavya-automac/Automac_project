from django.contrib.postgres.fields import ArrayField
from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver
from Automac_app.models import Machine_Kpi_List
import time

class MachineDetails(models.Model):
    objects = models.Manager()
    db_timestamp=models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField()
    test_timestamp = models.CharField(max_length=250,default='NA')
    machine_id = models.CharField(max_length=150)
    machine_location = models.CharField(max_length=250)
    digital_input = ArrayField(models.BooleanField())
    digital_output = ArrayField(models.BooleanField())
    analog_input = ArrayField(models.DecimalField(max_digits=10, decimal_places=2))
    analog_output = ArrayField(models.DecimalField(max_digits=10, decimal_places=2))
    other = ArrayField(models.CharField(max_length=100, default=True))

    class Meta:
        app_label = 'Automac_machines_app'
        db_table = 'machines_schema"."machinedetails_table'

    def __str__(self):
        # return "%s,%s %s" % (self.db_timestamp, self.machine_id,self.timestamp)
        return "%s,%s %s %s" % (self.db_timestamp, self.machine_id,self.timestamp,self.test_timestamp)

class Machine_KPI_Data(models.Model):
    machine_id=models.CharField(max_length=150)
    kpi_id=models.ForeignKey(Machine_Kpi_List,null=True,blank=True,on_delete=models.CASCADE)
    kpi_data=models.CharField(max_length=150)
    timestamp= models.DateTimeField()

    class Meta:
        app_label = 'Automac_machines_app'
        db_table = 'machines_schema"."Machine_KPI_Data'

    def __str__(self):
        # return "%s,%s %s" % (self.db_timestamp, self.machine_id,self.timestamp)
        return "%s %s %s" % (self.machine_id, self.timestamp, self.kpi_id)





#
# from Automac_app import  calculations
#
# @receiver(post_save,sender=MachineDetails)
# def signal(sender,instance,created,**kwargs):
#     if created:
#
#         print("new data arrived")
#         machine=instance.machine_id
#         print('instanceee',instance)
#         print('machine......',machine)
#
#         calculations.kpi_data_to_database(instance)
#         # signal_data = kpis.get_kpis_data(machine)
#         # print('signalllllllllllllll',signal_data)




# from . import kpi_websocket
#
# @receiver(post_save,sender=Machine_KPI_Data)
# def kpisignal(sender,instance,created,**kwargs):
#     if created:
#
#         print("new data arrived")
#         machine_id=instance.machine_id
#         kpi_websocket.kpi_socket(machine_id)