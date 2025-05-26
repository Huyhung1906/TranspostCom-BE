from rest_framework import serializers
from .models import Trip
from driver.serializers import DriverSerializer
from vehicle.serializers import VehicleSerializer
from route.serializers import RouteSerializer
from driver.models import Driver
from vehicle.models import Vehicle
from route.models import Route

class TripSerializer(serializers.ModelSerializer):
    driver = DriverSerializer(read_only=True)
    vehicle = VehicleSerializer(read_only=True)
    route = RouteSerializer(read_only=True)
    total_tickets = serializers.IntegerField(read_only=True)
    sold_tickets = serializers.IntegerField(read_only=True)
    driver_id = serializers.PrimaryKeyRelatedField(
        queryset=Driver.objects.all(), write_only=True, source='driver'
    )
    vehicle_id = serializers.PrimaryKeyRelatedField(
        queryset=Vehicle.objects.all(), write_only=True, source='vehicle'
    )
    route_id = serializers.PrimaryKeyRelatedField(
        queryset=Route.objects.all(), write_only=True, source='route'
    )

    class Meta:
        model = Trip
        fields = [
            'id',
            'driver', 'driver_id',
            'vehicle', 'vehicle_id',
            'route', 'route_id',
            'departure_time',
            'arrival_time',
            'total_tickets',
            'sold_tickets',
            'price',
            'notes',
            'is_active'
        ]