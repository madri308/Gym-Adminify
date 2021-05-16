from rest_framework import serializers
from .models import Activity, Service, Teacher, Client #, Schedule, ActivityHasClient

from gymClients.serializers import ClientSerializer, ClientNameSerializer
from gymServices.serializers import ServiceSerializer
from gymTeachers.serializers import TeacherSerializer
from AdmSchedule.serializers import ScheduleSerializer

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
            "schedule",
        )
class ScheduleActivitiesSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.name',read_only=True)
    teacher_name = serializers.CharField(source='teacher.person.name',read_only=True)
    schedule = ScheduleSerializer(many=False)
    class Meta:
        model = Activity
        fields = (
            "id",
            "dayofweek",
            "startime",
            "endtime",
            "service_name",
            "teacher_name", 
            "schedule",
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