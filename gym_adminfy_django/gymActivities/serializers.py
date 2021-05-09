from rest_framework import serializers
from .models import Activity, ActivityHasClient, Service, Teacher, Client #, Schedule, ActivityHasClient

from gymClients.serializers import ClientSerializer
from gymServices.serializers import ServiceSerializer
from gymTeachers.serializers import TeacherSerializer

class ActivityHasClientSerializer(serializers.ModelSerializer):
    client = ClientSerializer(many=True)
    class Meta:
        model = ActivityHasClient
        fields = (
            "id",
            "activity",
            "client"
        )

class ActivitiesSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(many=False)
    teacher = TeacherSerializer(many=False)
    class Meta:
        model = Activity
        fields = (
            "capacity",
            "dayofweek",
            "startime",
            "endtime",
            "service",
            "teacher"
            #,"schedule"
        )

