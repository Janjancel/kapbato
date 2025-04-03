from rest_framework import serializers
from ..models import Cart, CartItem
from .antique_serializers import AntiqueSerializer  # Import the AntiqueSerializer

class CartItemSerializer(serializers.ModelSerializer):
    antique = AntiqueSerializer()  # Include the AntiqueSerializer in CartItemSerializer

    class Meta:
        model = CartItem
        fields = ['id', 'quantity', 'antique']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)  # Include all cart items

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items']
