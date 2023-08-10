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

def all_topics(payload1,topic):
    if topic == 'maithri/abu_dabhi':
        conversion_file.store_data(payload1)
    elif topic == 'Topic_name':
        conversion_file.store_data(payload1)
    elif topic == 'Maithri/Device_7inch':
        conversion_file.MID004_store_data(payload1)