from rest_framework import serializers
from .models import Client,Schedule, Service, Teacher, Client

from gymServices.serializers import ServiceSerializer
from gymTeachers.serializers import TeacherSerializer

class ActivitiesSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(many=False)
    teacher = TeacherSerializer(many=False)
    clientstate = serializers.CharField(read_only=True)
    class Meta:
        model = Activity
        fields = (
            "name",
            "capacity",
            "dayofweek",
            "startime",
            "endtime",
            "service",
            "teacher"
            #,"schedule"
        )

class ActivityHasClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity_has_Client