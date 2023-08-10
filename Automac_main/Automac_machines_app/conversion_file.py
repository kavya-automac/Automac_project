import json
from django.apps import apps


def store_data(payload1):

    payload = json.loads(payload1)
    # print('payload',payload)

    # Extract the data from the JSON payload
    timestamp = payload['timestamp']
    machine_id = payload['info']['mid']
    machine_location = payload['info']['location']
    digital_input =[payload.get('LP1'),payload.get('LP2'),payload.get('HP1'),payload.get('HP2'),payload.get('Dosing'),payload.get('3PhasePreventer')]
    digital_output =[payload.get('Compressor_1'),payload.get('Compressor_2'),payload.get('Pump1'),payload.get('Pump2'),payload.get('Pump3')]
    analog_input = [payload.get('Temperature'),payload.get('Humidity')]
    analog_output = [payload.get('Flow')]
    other=[
        payload.get('Water_Level'),
        payload.get('set_points ',{}).get('set_temp'),
        payload.get('set_points ',{}).get('set_hum'),
        payload.get('THSensor_Status'),
        payload.get('Temp_Subzero'),
        payload.get('Hum_Suzero')
    ]
    print('digital_input abb',digital_input)


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



def MID004_store_data(payload1):

    payload = json.loads(payload1)
    # print('payload',payload)

    # Extract the data from the JSON payload
    timestamp = payload['timestamp']
    machine_id = payload['info']['mid']
    machine_location = payload['info']['location']
    digital_input =[payload.get('Dosing')]
    digital_output =[payload.get('Compressor_1'),payload.get('Pump')]
    analog_input = [payload.get('Temperature'),payload.get('Humidity')]
    analog_output = [payload.get('Flow')]
    other=[
        payload.get('Water_Level'),
        payload.get('set_points ',{}).get('set_temp'),
        payload.get('set_points ',{}).get('set_hum'),
        payload.get('THSensor_Status'),
        payload.get('Temp_Subzero'),
        payload.get('Hum_Suzero')
    ]
    print('digital_input',digital_input)


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

