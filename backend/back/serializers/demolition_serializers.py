from rest_framework import serializers
from ..models import DemolitionRequest

class DemolitionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemolitionRequest
        fields = '__all__'
