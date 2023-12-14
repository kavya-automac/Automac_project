import json

from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
from . import kpi_websocket
import schedule
import time
from asgiref.sync import sync_to_async
import websockets
from .mqtt import client

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Add the consumer to the "chat" channel group
        # print(self.scope["user"])
        # print('paramsssssssssssss',self.scope["headers"])
        # print('scope', self.scope)
        # print('qery_stringggg', self.scope['query_string'].decode())

        client.publish("ws_con", "Connected")

        query_string=self.scope['query_string'].decode()
        machine_id = query_string.split('=')[1].split('&')[0]
        print('machine_id connect ',machine_id)



        # paramsssssssssssss [(b'sec-websocket-version', b'13'), (b'sec-websocket-key', b'PID+IdLq/ts0PQ8qVc2xUQ=='), (b'connection', b'Upgrade'), (b'upgrade', b'websocket'),
 # (b'sec-websocket-extensions', b'permessage-deflate; client_max_window_bits'), (b'host', b'127.0.0.1:8000')]

        await self.channel_layer.group_add(str(machine_id)+'_io', self.channel_name)
        # group_name=self.scope["url_route"]["kwargs"]["group_name"]
        # print('group_name',group_name)
        await self.accept()


    async def disconnect(self, close_code):
        client.publish("ws_con", "Disconnected")


        query_string = self.scope['query_string'].decode()
        machine_id = query_string.split('=')[1]
        print('idddddddddddddddddddddddd',machine_id)
        await self.channel_layer.group_discard(str(machine_id)+'_io', self.channel_name)

        # Remove the consumer from the "chat" channel group
        # await self.channel_layer.group_discard("mqtt_data", self.channel_name)


    async def receive(self, text_data):
        print('text',text_data)
        print('reciver ........scope', self.scope)


        # Send the processed data to the connected WebSocket clients
        await self.channel_layer.group_send("mqtt_data", {
            "type": "chat.message",
            "text": text_data  # Send the processed data as the message
        })
        # print('receive text_data',text_data)
        # await asyncio.sleep(5)

    async def chat_message(self, event):
        # print('ppppppp',self.scope.get('machine_id'))
        # print('selff',self)
        # # selff <Automac_machines_app.consumers.ChatConsumer object at 0x0000022389CD89D0>
        # print('scope',self.scope)
        # print('qery_stringggg',self.scope['query_string'].decode())
        print('event' , event)
        print('event text' , event["text"])

        try:
            # Send the received data to the WebSocket connection
            await self.send(text_data=event["text"])
            print("eventtttttttttttttttttttttttttt")
            # await self.send(text_data=json.dumps(event["text"]))
            await asyncio.sleep(1)
        except Exception as e:
            print("chat message error - ", e)

#
# # @sync_to_async
# def test(self):
#     # machine_id = 'MI'
#     print('task function')
#
#
# class myscheduler:
#     def __init__(self,machine):
#         self.machine_id=machine
#         print(self.machine_id)
#         # Initialize any class-specific variables here
#         # self.counter = 0
#         pass
#
#     async def my_task(self):
#         await kpi_websocket.kpi_socket(self.machine_id)
#         # await kpi_websocket.kpi_socket(self.machine_id)
#         # loop = asyncio.new_event_loop()
#         # asyncio.set_event_loop(loop)
#         # loop.run_until_complete(kpi_websocket.kpi_socket(self.machine_id))
#
#
#     def start_scheduling(self):
#         # Schedule my_task to run every 2 seconds
#         schedule.every(2).seconds.do(self.my_task)
#
#         while True:
#             schedule.run_pending()
#             time.sleep(1)
#


class KpiConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        try:
            client.publish("ws_test","connectedddd")
            query_string = self.scope['query_string'].decode()
            print('query_string',query_string)
            machine_id = query_string.split('=')[1].split('&')[0]
            username = query_string.split('=')[2]
            print('username',username)
            # if not machine_id:
            #     await self.close()
            #     return
            await self.channel_layer.group_add(str(machine_id)+'_kpi', self.channel_name)

            await self.accept()

            # Start calling kpi_socket function periodically
            self.machine_id = machine_id
            self.username=username
            self.scheduler_task = asyncio.create_task(self.schedule_kpi_socket())
        except Exception as e:
            print("errorrrrr",e)

    async def disconnect(self, close_code):
        # Cancel the scheduler task when disconnecting
        client.publish("ws_test", "disconnected")
        if hasattr(self, 'scheduler_task'):# hasattr() function is an inbuilt utility function,\
            # which is used to check if an object has the given named attribute and return true if present, else false.
            self.scheduler_task.cancel()

        await self.channel_layer.group_discard(str(self.machine_id)+'_kpi', self.channel_name)

    async def schedule_kpi_socket(self):
        while True:
            try:
                print("-----------------------------------------------")
                print("-----------------------------------------------")
                await kpi_websocket.kpi_socket(self.username,self.machine_id)
                # Adjust the sleep duration as needed (e.g., call every 10 seconds)
                await asyncio.sleep(2)
            except asyncio.CancelledError:
                # Task was canceled due to disconnection
                break

    async def kpiweb(self, event):
        try:
            await self.send(text_data=event["text"])
        except Exception as e:
            print("kpi message error - ", e)

