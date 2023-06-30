from rest_framework import serializers
from .models import *
class machineSerializer(serializers.ModelSerializer):
    class Meta:
        model=MachineDetails
        fields = "__all__"