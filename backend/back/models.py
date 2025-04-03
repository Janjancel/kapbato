from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now

User = get_user_model()

# Ensure there's a valid default user for testing
def get_default_user():
    first_user = User.objects.first()
    return first_user.id if first_user else None  # Handle case if no user exists


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class HeritageHouse(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    image = models.ImageField(upload_to='heritage_images/', null=True, blank=True)

    def __str__(self):
        return self.name


# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="userprofile")
#     profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

#     def __str__(self):
#         return self.user.username

User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="userprofile")
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)

    def __str__(self):
        return self.user.username


class DemolitionRequest(models.Model):
    where = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='demolitions/', null=True, blank=True)

    def __str__(self):
        return self.name


class SellRequest(models.Model):
    where = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='sell_images/')

    def __str__(self):
        return self.name


class Antique(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    origin = models.CharField(max_length=255, blank=True, null=True)
    age = models.PositiveIntegerField(help_text="Age of the antique in years", blank=True, null=True)
    image = models.ImageField(upload_to="antiques/", blank=True, null=True)
    added_on = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural = "Antiques"  # ✅ Better admin display

    def __str__(self):
        return f"{self.name} - ${self.price}"  # ✅ More descriptive


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")  # ✅ Ensure only one cart per user

    def __str__(self):
        return f"{self.user.username}'s Cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    antique = models.ForeignKey(Antique, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'antique')  # ✅ Ensure no duplicate items in the same cart

    def __str__(self):
        return f"{self.antique.name} ({self.quantity}) in {self.cart.user.username}'s Cart"
