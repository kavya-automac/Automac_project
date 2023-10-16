from rest_framework import serializers
from .models import *
# machineSerializer this is used in history page don't change any field
class machineSerializer(serializers.ModelSerializer):# iostatus # Trail_details
    class Meta:
        model=MachineDetails
        # fields = "__all__"
        fields = ('db_timestamp','timestamp','machine_id','machine_location','digital_input','digital_output','analog_input','analog_output','other')

class machineSerializer_two(serializers.ModelSerializer):
    class Meta:
        model=MachineDetails
        fields=('timestamp','machine_id','machine_location')


class analog_ip_op_Serializer(serializers.ModelSerializer):
    class Meta:
        model=MachineDetails
        fields=('timestamp','machine_id','machine_location','analog_input','analog_output')

class kpi_data_Serializer(serializers.ModelSerializer): #  for kpis
    class Meta:
        model=Machine_KPI_Data
        fields='__all__'


class kpi_cummulative_serilaizer(serializers.ModelSerializer):
    class Meta:
        model=Machine_KPI_Data
        fields=('machine_id','kpi_id','kpi_data')

