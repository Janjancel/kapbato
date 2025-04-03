# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from .models import DemolitionRequest, SellRequest

# class DashboardConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.channel_layer.group_add("dashboard_updates", self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard("dashboard_updates", self.channel_name)

#     async def receive(self, text_data):
#         pass  # We don't need to handle messages from the frontend

#     async def send_update(self, event):
#         demolitions = await self.get_demolition_count()
#         sales = await self.get_sell_count()

#         await self.send(text_data=json.dumps({"demolitions": demolitions, "sales": sales}))

#     async def get_demolition_count(self):
#         return await self.get_count(DemolitionRequest)

#     async def get_sell_count(self):
#         return await self.get_count(SellRequest)

#     async def get_count(self, model):
#         return await self.get_model_count(model)

#     @staticmethod
#     async def get_model_count(model):
#         return await model.objects.acount()

# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.layers import get_channel_layer

# class DashboardConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.channel_layer.group_add("dashboard_updates", self.channel_name)
#         await self.accept()
#         print("WebSocket connected")

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard("dashboard_updates", self.channel_name)
#         print("WebSocket disconnected")

#     async def send_update(self, event):
#         await self.send(text_data=json.dumps({
#             "demolitions": event["demolitions"],
#             "sales": event["sales"],
#         }))
#         print("Sent WebSocket update:", event)


from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

class DashboardConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        
        # Require authentication
        if isinstance(self.user, AnonymousUser):
            await self.close()
            return

        await self.accept()

    async def receive_json(self, content, **kwargs):
        await self.send_json({"message": "Real-time data!"})
