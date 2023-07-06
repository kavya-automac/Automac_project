from django.contrib.postgres.fields import ArrayField
from django.db import models



class Line_List(models.Model):
    objects = models.Manager()
    line_name=models.CharField(max_length=100)

    class Meta:
        app_label = 'Automac_app'
        db_table = 'users_schema"."Line_List'

    def __str__(self):
        return self.line_name


class Model_List(models.Model):
    objects = models.Manager()

    model_name=models.CharField(max_length=100)

    class Meta:
        app_label = 'Automac_app'
        db_table = 'users_schema"."Model_List'

    def __str__(self):
        return self.model_name


class Plant_List(models.Model):
    objects = models.Manager()
    plant_name=models.CharField(max_length=100)
    plant_location=models.CharField(max_length=100)

    class Meta:
        app_label = 'Automac_app'
        db_table = 'users_schema"."Plant_List'

    def __str__(self):
        return self.plant_name


class Company_List(models.Model):
    objects = models.Manager()
    company_name=models.CharField(max_length=100)
    company_location=models.CharField(max_length=100)

    class Meta:
        app_label = 'Automac_app'
        db_table = 'users_schema"."Company_List'

    def __str__(self):
        return self.company_name


class Machine_Kpi_List(models.Model):
    objects = models.Manager()
    kpi_name=models.CharField(max_length=100)
    kpi_data=models.IntegerField()
    kpi_unit=models.CharField(max_length=10,blank=True)

    class Meta:
        app_label = 'Automac_app'
        db_table = 'users_schema"."Machine_Kpi_List'

    def __str__(self):
        return self.kpi_name




class Machines_List(models.Model):
    objects = models.Manager()
    machine_image=models.ImageField(upload_to='images',blank=True)
    machine_name=models.CharField(max_length=100)
    machine_location=models.CharField(max_length=100)
    digital_input= ArrayField(models.CharField(max_length=100,blank=True))
    digital_output= ArrayField(models.CharField(max_length=100,blank=True))
    analog_input = ArrayField(models.CharField(max_length=100,blank=True))
    analog_output = ArrayField(models.CharField(max_length=100,blank=True))
    date_of_installation=models.CharField(max_length=100,blank=True)
    machine_state=models.CharField(max_length=100)

    class Meta:
        app_label = 'Automac_app'
        db_table = 'users_schema"."Machines_List'

    def __str__(self):
        return self.machine_name