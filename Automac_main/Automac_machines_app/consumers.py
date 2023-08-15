import json

from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Add the consumer to the "chat" channel group
        # print(self.scope["user"])
        # print('paramsssssssssssss',self.scope["headers"])
        # print('scope', self.scope)
        # print('qery_stringggg', self.scope['query_string'].decode())
        query_string=self.scope['query_string'].decode()
        machine_id = query_string.split('=')[1]
        # print('machine_id',machine_id)



        # paramsssssssssssss [(b'sec-websocket-version', b'13'), (b'sec-websocket-key', b'PID+IdLq/ts0PQ8qVc2xUQ=='), (b'connection', b'Upgrade'), (b'upgrade', b'websocket'),
 # (b'sec-websocket-extensions', b'permessage-deflate; client_max_window_bits'), (b'host', b'127.0.0.1:8000')]

        await self.channel_layer.group_add(machine_id, self.channel_name)
        # group_name=self.scope["url_route"]["kwargs"]["group_name"]
        # print('group_name',group_name)
        await self.accept()


    async def disconnect(self, close_code):
        # Remove the consumer from the "chat" channel group
        await self.channel_layer.group_discard("mqtt_data", self.channel_name)

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


        # Send the received data to the WebSocket connection
        await self.send(text_data=event["text"])
        # print(event)
        # await self.send(text_data=json.dumps(event["text"]))
        await asyncio.sleep(1)

