from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Add the consumer to the "chat" channel group
        await self.channel_layer.group_add("mqtt_data", self.channel_name)
        # group_name=self.scope["url_route"]["kwargs"]["group_name"]
        # print('group_name',group_name)
        await self.accept()


    async def disconnect(self, close_code):
        # Remove the consumer from the "chat" channel group
        await self.channel_layer.group_discard("mqtt_data", self.channel_name)

    async def receive(self, text_data):
        # Handle received data from the WebSocket connection
        # You can perform any required processing or logic here
        # For example, you can save the received data to the database
        # or perform some calculations on the data

        # Send the processed data to the connected WebSocket clients
        await self.channel_layer.group_send("mqtt_data", {
            "type": "chat.message",
            "text": text_data  # Send the processed data as the message
        })
        # await asyncio.sleep(5)

    async def chat_message(self, event):
        # Send the received data to the WebSocket connection
        await self.send(text_data=event["text"])
        # await asyncio.sleep(2)

