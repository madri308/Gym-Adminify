from rest_framework import serializers
from .models import ActivityBU

class ActivitiesBUSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityBU
        fields = (
            "id",
            "capacity",
            "dayofweek",
            "startime",
            "endtime",
            "service",
            "teacher", 
            "schedule",
            "dayofmonth",
            "state",
            "creator",
        )