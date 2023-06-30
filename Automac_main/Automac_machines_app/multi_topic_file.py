from . import conversion_file


topics=['maithri/abu_dabhi']

def all_topics(payload1) :
    if 'maithri/abu_dabhi' in  topics:
        conversion_file.store_data(payload1)

    else:
        pass