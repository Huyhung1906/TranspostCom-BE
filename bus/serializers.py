from rest_framework import serializers
from .models import Bus

class busserializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = ['id','name','type','chair','licenseplate']