from django.contrib.postgres.fields import ArrayField
from django.db import models

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
