from django.contrib import admin
from .models import Item, HeritageHouse, DemolitionRequest, SellRequest, Antique
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(Item)

admin.site.register(HeritageHouse)

admin.site.register(DemolitionRequest)
admin.site.register(SellRequest)

from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile

# Extend UserAdmin to display UserProfile fields
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False

# Extend User admin to show UserProfile
class CustomUserAdmin(admin.ModelAdmin):
    inlines = [UserProfileInline]

# Unregister default User and re-register with custom admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)  # Register UserProfile separately


from django.contrib import admin
from .models import Antique

@admin.register(Antique)
class AntiqueAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "origin", "age", "added_on")
    search_fields = ("name", "origin")

from .models import Cart, CartItem
admin.site.register(Cart)
admin.site.register(CartItem)