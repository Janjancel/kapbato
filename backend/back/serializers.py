from rest_framework import serializers
from .models import Item, HeritageHouse

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class HeritageHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeritageHouse
        fields = ['name', 'latitude', 'longitude', 'description', 'image']



from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'surname']  # Include surname and other fields as needed

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            surname=validated_data.get('surname', '')
        )
        return user


# from rest_framework import serializers
# from .models import UserProfile

# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = ['name', 'profile_picture']

from rest_framework import serializers
from .models import DemolitionRequest

class DemolitionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemolitionRequest
        fields = '__all__'

from rest_framework import serializers
from .models import SellRequest

class SellRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellRequest
        fields = '__all__'


# from rest_framework import serializers
# from django.contrib.auth.models import User  # Ensure you are using the correct model

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ["id", "username", "email", "date_joined"]

# serializers.py
from rest_framework import serializers
from back.models import Antique

class AntiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Antique
        fields = ['id', 'name', 'description', 'price', 'image']  # Include fields that you want to return



# serializers.py
from rest_framework import serializers
from .models import CartItem
from back.serializers import AntiqueSerializer  # Import the AntiqueSerializer

class CartItemSerializer(serializers.ModelSerializer):
    antique = AntiqueSerializer()  # Include the AntiqueSerializer in the CartItemSerializer

    class Meta:
        model = CartItem
        fields = ['id', 'quantity', 'antique']  # Include the fields you need for CartItem

from .models import Cart
class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)  # Include all cart items for the user

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items']

from rest_framework import serializers
from django.contrib.auth import get_user_model
from back.models import UserProfile

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="user.get_full_name", read_only=True)  # ✅ Correct
    username = serializers.CharField(source="user.username", read_only=True)  # ✅ Correct
    email = serializers.EmailField(source="user.email", read_only=True)  # ✅ Correct
    profile_picture = serializers.ImageField(required=False)  # ✅ Correct

    class Meta:
        model = UserProfile
        fields = ["full_name", "username", "email", "profile_picture"]  # ✅ No `name`





class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ["id", "username", "email", "userprofile"]
