from rest_framework import serializers
from .models import Cars

class CarSerializer(serializers.Serializer):

    class Meta:
        model = Cars
        fields = ['CarName', 'ModelName', 'CarNumber', 
                    'Features', 'IsAvailable', 'CarImage', 
                    'fuelConsumption', 'carInsurance', 'CostPerDay']


