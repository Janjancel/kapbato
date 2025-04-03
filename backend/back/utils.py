import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import DemolitionRequest, SellRequest  # Ensure correct import

async def send_dashboard_update():
    """Sends real-time dashboard updates via WebSocket."""
    channel_layer = get_channel_layer()
    demolition_count = await DemolitionRequest.objects.acount()
    sell_count = await SellRequest.objects.acount()

    await channel_layer.group_send(
        "dashboard_updates",
        {
            "type": "send_update",
            "demolitions": demolition_count,
            "sales": sell_count,
        },
    )



import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import DemolitionRequest, SellRequest  # Ensure correct import

def send_dashboard_update():
    """Sends real-time dashboard updates via WebSocket."""
    channel_layer = get_channel_layer()
    demolition_count = DemolitionRequest.objects.count()
    sell_count = SellRequest.objects.count()

    async_to_sync(channel_layer.group_send)(
        "dashboard_updates",
        {
            "type": "send_update",
            "demolitions": demolition_count,
            "sales": sell_count,
        },
    )
