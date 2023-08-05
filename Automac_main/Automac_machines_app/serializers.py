from rest_framework import serializers
from .models import *
# machineSerializer this is used in history page don't change any field
class machineSerializer(serializers.ModelSerializer):
    class Meta:
        model=MachineDetails
        # fields = "__all__"
        fields = ('db_timestamp','timestamp','machine_id','machine_location','digital_input','digital_output','analog_input','analog_output')

class machineSerializer_two(serializers.ModelSerializer):
    class Meta:
        model=MachineDetails
        fields=('timestamp','machine_id','machine_location')


class analog_ip_op_Serializer(serializers.ModelSerializer):
    class Meta:
        model=MachineDetails
        fields=('timestamp','machine_id','machine_location','analog_input','analog_output')

