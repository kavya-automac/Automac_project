from . import conversion_file


# topics=['maithri/abu_dabhi','Topic_name','Maithri/Device_7inch']

# def all_topics(payload1,topic) :
#     if 'maithri/abu_dabhi' in  topics:
#         conversion_file.store_data(payload1)
#     if 'Topic_name' in  topics:
#         conversion_file.store_data(payload1)
#     if 'Maithri/Device_7inch' in  topics:
#         conversion_file.MID004_store_data(payload1)
#
#     else:
#         pass


def all_topics(mqtt_machines_data,topic):
    # print("topics in all topics file befor",topic)
    if topic == 'maithri/abu_dabhi':
        # print('topic in maithri',topic)
        conversion_file.store_data(mqtt_machines_data)
    elif topic == 'Topic_name':
        # print('topic in Topic_name',topic)

        # print("all_topics Topic_name ")
        conversion_file.store_data(mqtt_machines_data)
    elif topic == 'Maithri/Device_7inch':
        # print('topic in Device_7inch',topic)

        conversion_file.MID004_store_data(mqtt_machines_data)
    elif topic == 'demo_app' or topic == 'CSD' or topic == 'Maithri_test':
        # print('topic in demo_app',topic)

        conversion_file.mqtt_test_machine_data(mqtt_machines_data)
    # print("topics in all topics file afterrrrr",topic)


