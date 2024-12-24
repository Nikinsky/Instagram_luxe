# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))



















#import asyncio
# from channels.generic.websocket import AsyncWebsocketConsumer
# import json
#
#
# class TimerConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.accept()
#         self.timer_running = False
#         self.current_time = 0
#
#     async def disconnect(self, close_code):
#         self.timer_running = False
#
#
#     async def receive(self, text_data):
#         data = json.loads(text_data)
#
#         if data.get("action") == "start" and data.get("time") is not None:
#             self.timer_running = True
#             self.current_time = int(data["time"])
#             asyncio.create_task(self.start_countdown())
#
#         elif data.get("action") == "stop":
#             self.timer_running = False
#             await self.send(text_data=json.dumps({
#                 "massage": "Таймер остановлен",
#                 "time": self.current_time
#             }))
#
#     async def start_countdown(self):
#         while self.timer_running and self.current_time > 0:
#             await self.send(text_data=json.dumps({
#                 "time": self.current_time
#             }))
#             self.current_time -= 1
#             await asyncio.sleep(1)
#
#         if self.timer_running and self.current_time == 0:
#             await self.send(text_data=json.dumps({
#                 "massage": "Время вышло!",
#                 "time": 0
#             }))
#             self.timer_running = False
#
