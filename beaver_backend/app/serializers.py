from rest_framework import serializers
from .models import Neighborhood

class NeighborhoodSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Neighborhood
        fields = ['name']