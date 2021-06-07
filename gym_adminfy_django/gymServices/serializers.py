from rest_framework import serializers
from .models import Service

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = (
            "id",
            "name",
            "description",
            "hourfee",
            "get_absolute_url",
        )

class IdServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = (
            "id",
        )
class NameServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = (
            "name",
        )