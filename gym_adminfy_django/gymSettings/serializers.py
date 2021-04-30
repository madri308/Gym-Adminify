from rest_framework import serializers
from .models import Gym, Room, Config

class ConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = (
            "id",
            "effectivedate",
            "capacitypercentage",
            "timeperday",
            "get_absolute_url"
        )