from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import User



class Line_List(models.Model):
    objects = models.Manager()
    line_name=models.CharField(max_length=100,null=True,blank=True)

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
        return str(self.model_name)



class Plant_List(models.Model):
    objects = models.Manager()
    plant_name=models.CharField(max_length=100)
    plant_location=models.CharField(max_length=100)

    class Meta:
        app_label = 'Automac_app'
        db_table = 'users_schema"."Plant_List'

    def __str__(self):
        return str(self.plant_name)


class Company_List(models.Model):
    objects = models.Manager()
    company_name=models.CharField(max_length=100)
    company_location=models.CharField(max_length=100)

    class Meta:
        app_label = 'Automac_app'
        db_table = 'users_schema"."Company_List'

    def __str__(self):
        return str(self.company_name)



class Machine_Kpi_List(models.Model):
    objects = models.Manager()
    kpi_name=models.CharField(max_length=100)
    kpi_data=models.IntegerField()
    kpi_unit=models.CharField(max_length=10,blank=True)

    class Meta:
        app_label = 'Automac_app'
        db_table = 'users_schema"."Machine_Kpi_List'

    def __str__(self):
        return str(self.kpi_name)




class Machines_List(models.Model):
    objects = models.Manager()
    machine_image=models.ImageField(upload_to='images',blank=True)
    machine_name=models.CharField(max_length=100)
    machine_id=models.CharField(max_length=100,blank=True)

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
        return str(self.machine_name)
#


class all_Machine_data(models.Model):
    objects = models.Manager()
    user_name=models.ForeignKey(User,on_delete=models.CASCADE)
    company_name=models.ForeignKey(Company_List,on_delete=models.CASCADE)
    # company_name=models.CharField(max_length=50,blank=True)
    plant_name = models.ForeignKey(Plant_List,null=True,blank=True, on_delete=models.CASCADE)
    machine_id = models.ForeignKey(Machines_List, on_delete=models.CASCADE)
    model_name = models.ForeignKey(Model_List, on_delete=models.CASCADE)
    line_name = models.ForeignKey(Line_List, null=True,blank=True,on_delete=models.CASCADE)

    class Meta:
        app_label = 'Automac_app'
        db_table = 'users_schema"."all_Machine_data'

    def __str__(self):
        return str(self.machine_id)











