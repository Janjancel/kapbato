# from django.db.models.signals import post_save
# from django.contrib.auth.models import User
# from django.dispatch import receiver
# from .models import UserProfile

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.userprofile.save()

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile  # Import your UserProfile model

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()



# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import DemolitionRequest, SellRequest
# from .utils import send_dashboard_update  # Import from utils.py

# @receiver(post_save, sender=DemolitionRequest)
# def update_dashboard_on_demolition_request(sender, instance, **kwargs):
#     send_dashboard_update()  # Call the function after save

# @receiver(post_save, sender=SellRequest)
# def update_dashboard_on_sell_request(sender, instance, **kwargs):
#     send_dashboard_update()  # Call the function after save

from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import DemolitionRequest, SellRequest

@receiver(post_save, sender=DemolitionRequest)
@receiver(post_save, sender=SellRequest)
def update_dashboard(sender, instance, **kwargs):
    """Send WebSocket update when a new request is added"""
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
    print("Signal triggered WebSocket update")
