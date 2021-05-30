from rest_framework import serializers
from .models import Activity, Service, Teacher, Client #, Schedule, ActivityHasClient

from gymClients.serializers import ClientSerializer, ClientNameSerializer
from gymServices.serializers import ServiceSerializer
from gymTeachers.serializers import TeacherSerializer

class ActivitiesSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(many=False)
    teacher = TeacherSerializer(many=False)
    client = ClientNameSerializer(many=True)
    class Meta:
        model = Activity
        fields = (
            "id",
            "capacity",
            "dayofweek",
            "startime",
            "endtime",
            "service",
            "teacher", 
            "client", 
            "get_absolute_url"
            #,"schedule"
        )

# class ActivityHasClientSerializer(serializers.ModelSerializer):
#     client = ClientSerializer(many=False)
#     activity = ActivitiesSerializer(many=False)
#     class Meta:
#         model = ActivityHasClient
#         fields = (
#             "id",
#             "activity",
#             "client"
#         )