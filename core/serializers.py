from rest_framework import serializers

from .models import * 

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vehicle
        exclude=['created_at', 'updated_at', 'deleted_at']

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model=Trip
        fields='__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields='__all__'

class MaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Maintenance
        fields='__all__'