import json
from django.utils import timezone
from django.apps import apps


def store_data(payload1):

    payload = json.loads(payload1)
    # print('payload',payload)

    # Extract the data from the JSON payload
    timestamp = payload['timestamp']
    machine_id = payload['info']['mid']
    machine_location = payload['info']['location']
    digital_input =[payload['Temperature'],payload['Humidity'],payload['LP1'],payload['LP2'],payload['HP1'],payload['HP2'],payload['Dosing'],payload['3PhasePreventer']]
    digital_output =[payload['Compressor_1'],payload['Compressor_2'],payload['Pump1'],payload['Pump2'],payload['Pump3']]
    analog_input = []
    analog_output = [payload['Flow']]
    other=[
        payload['Water_Level'],
        payload['set_points ']['set_temp'],
        payload['set_points ']['set_hum'],
        payload['THSensor_Status'],
        payload['Temp_Subzero'],
        payload['Hum_Suzero']
    ]



    MachineDetails = apps.get_model('Automac_machines_app', 'MachineDetails')


    # for v in digital_output:
    #     if v=="on" :
    #         v=True
    #     if v=="off":
    #         v= False
    #     print('v',v)

    digital_input =[True if value == 'on' else False for value in digital_input]

    digital_output = [True if value == 'on' else False for value in digital_output]

    # Create an instance of the SensorData model
    sensor_data = MachineDetails(
       # timestamp=timezone.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f'),
       timestamp=timestamp,
       machine_id=machine_id,
       machine_location=machine_location,
       digital_input=digital_input,
       digital_output=digital_output,
       analog_input=analog_input,
       analog_output=analog_output,
       other=other
    )

    # Save the instance to the database
    sensor_data.save()

