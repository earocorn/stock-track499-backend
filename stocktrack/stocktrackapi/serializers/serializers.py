from rest_framework import serializers

from ..models.stocktrackuser import StockTrackUser
from ..models.examplemodel import ExampleModel

# We can choose to do classes or just put them all in here,
# probably classes to keep it neater

class StockTrackUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockTrackUser
        fields = ('__all__')

class ExampleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExampleModel
        fields = ('__all__')