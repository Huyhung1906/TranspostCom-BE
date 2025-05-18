from rest_framework import serializers
from .models import Vehicle

class vehicleserializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id','name','type','chair','licenseplate']