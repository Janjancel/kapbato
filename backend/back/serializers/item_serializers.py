from rest_framework import serializers
from ..models import Item, HeritageHouse

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class HeritageHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeritageHouse
        fields = ['name', 'latitude', 'longitude', 'description', 'image']
