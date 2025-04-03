from rest_framework import serializers
from ..models import SellRequest

class SellRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellRequest
        fields = '__all__'
