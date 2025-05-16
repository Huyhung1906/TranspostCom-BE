from rest_framework import serializers
from .models import Route

class routeserializer(serializers.ModelSerializer):
    code = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = Route
        fields = ['id','departure_point','destination_point','distance_km','estimated_time','description','is_active','code']