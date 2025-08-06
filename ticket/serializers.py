from rest_framework import serializers
from .models import Ticket
from trip.serializers import TripSerializer
class TicketSerializer(serializers.ModelSerializer):
    trip = TripSerializer(read_only=True)  # embed thông tin trip ở đây
    class Meta:
        model = Ticket
        fields = '__all__'
