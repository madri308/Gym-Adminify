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

class ConfigSerializerCapacity(serializers.ModelSerializer):
    class Meta:
        model = Config
        fields = (
            "capacitypercentage",
        )

class GymSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gym
        fields = (
            "id",
            "name",
            "tuitioncost",
            "config",
            "get_absolute_url"
        )
    
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = (
            "id",
            "name",
            "capacity",
            "gym",
            "schedule",
            "get_absolute_url"
        )