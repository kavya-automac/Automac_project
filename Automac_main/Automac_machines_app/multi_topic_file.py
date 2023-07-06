from . import conversion_file


topics=['maithri/abu_dabhi','Topic_name']

def all_topics(payload1) :
    if 'maithri/abu_dabhi' in  topics:
        conversion_file.store_data(payload1)
    if 'Topic_name' in  topics:
        conversion_file.store_data(payload1)

    else:
        pass