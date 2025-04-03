from rest_framework import serializers
from ..models import Antique

class AntiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Antique
        fields = ['id', 'name', 'description', 'price', 'image']
