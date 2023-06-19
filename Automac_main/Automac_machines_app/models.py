from django.contrib.postgres.fields import ArrayField
from django.db import models

class MachineDetails(models.Model):
    objects = models.Manager()
    timestamp = models.DateTimeField(auto_now_add=True)
    machine_id = models.CharField(max_length=150)
    machine_location = models.CharField(max_length=250)
    digital_input = ArrayField(models.BooleanField())
    digital_output = ArrayField(models.BooleanField())
    analog_input = ArrayField(models.DecimalField(max_digits=10, decimal_places=2))
    analog_output = ArrayField(models.DecimalField(max_digits=10, decimal_places=2))


    class Meta:
        app_label = 'Automac_machines_app'
        db_table = 'machines_schema"."machinedetails_table'

    # def __str__(self):  # to display the timestamp in admin page
    #     return str(self.timestamp)
    #

