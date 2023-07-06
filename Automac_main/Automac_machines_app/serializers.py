from rest_framework import serializers
from .models import *
class machineSerializer(serializers.ModelSerializer):
    class Meta:
        model=MachineDetails
        fields = "__all__"

class machineSerializer_two(serializers.ModelSerializer):
    class Meta:
        model=MachineDetails
        fields=('id','timestamp','machine_id','machine_location')

