from rest_framework import serializers

from .models import Car

class CarSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Car
        fields = ('make', 'model', 'average_rating', 'votes_num')
