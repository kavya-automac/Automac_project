import json

from channels.consumer import SyncConsumer,AsyncConsumer
from channels.exceptions import StopConsumer
from time import sleep
import asyncio
from channels.db import database_sync_to_async

from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models.signals import post_save

from . models import *

# data = machine_data.objects.filter(machine_id="ABD2").values().last()
# print('data',data)
from django.core.serializers import serialize



class MyAsyncConsumer(AsyncWebsocketConsumer):
    async def websocket_connect(self,event):

        print('websocket connected....', event)
        # await self.send({
        #         'type': 'websocket.accept',
        #      })
        await self.accept()
        self.send_data = True

        await self.send_updated_data()



    async def send_updated_data(self):
        while self.send_data:
            data = await self.get_data_from_database()

            # data_str = json.dumps(data)
            data_str = json.dumps(data, default=str)  # Convert to JSON string

            print('data', type(data_str))

            await self.send(text_data=data_str)

            await asyncio.sleep(2)




    @database_sync_to_async
    def get_data_from_database(self):
        # data = 'kavya'
        # data = machine_data.objects.filter(machine_id="ABD2")
        data = machine_data.objects.filter(machine_id="135BA28").values().last()

        print('get_data', data)
        print('type_data', type(data))


        return data

    async def websocket_receive(self,event):
        print('message received from client...',event)
        print(event['text'])


    async def websocket_disconnect(self,event):
        print('websocket Disconnected...',event)
        # raise StopConsumer()




