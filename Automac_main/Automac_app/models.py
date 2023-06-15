from django.db import models

# Create your models here.
# class user_details(models.Model):
#     objects = models.Manager()
#     username=models.CharField(max_length=100,null=False)
#     password=models.CharField(max_length=100,null=False)
#     email = models.CharField(max_length=100,null=False)
#
#     def __str__(self):   # to display the dept name in admin page
#         return self.username


class machine_data(models.Model):
    objects = models.Manager()
    machine_id = models.CharField(max_length=150)
    machine_location= models.CharField(max_length=250)
    timestamp= models.DateTimeField(auto_now_add=True)
    digital_input= models.BooleanField(default=False)
    digital_output= models.BooleanField(default=False)
    analog_input= models.IntegerField()
    analog_output= models.IntegerField()

    def __str__(self):   # to display the timestamp in admin page
             return  str(self.timestamp)

