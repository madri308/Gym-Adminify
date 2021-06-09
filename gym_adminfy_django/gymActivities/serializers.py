from rest_framework import serializers
from .models import Activity, Service, Teacher, Client #, Schedule, ActivityHasClient

from gymClients.serializers import ClientNameSerializer
from gymServices.serializers import NameServiceSerializer
from gymTeachers.serializers import TeacherNamesSerializer
from AdmSchedule.serializers import ScheduleSerializer

class ActivitiesSerializer(serializers.ModelSerializer):
    service = NameServiceSerializer(many=False)
    teacher = TeacherNamesSerializer(many=False)
    client = ClientNameSerializer(many=True)
    schedule = ScheduleSerializer(many=False)
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
            "dayofmonth",
        )

class SpecificDataActivitiesSerializer(serializers.ModelSerializer):
    client = ClientNameSerializer(many=True)
    teacher = TeacherNamesSerializer(many=False)
    class Meta:
        model = Activity
        fields = (
            "client",
            "dayofmonth",
            "teacher",
        )

class GeneralActivitiesSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.name',read_only=True)
    teacher = TeacherNamesSerializer(many=False)
    schedule = ScheduleSerializer(many=False)
    class Meta:
        model = Activity
        fields = (
            "dayofweek",
            "startime",
            "endtime",
            "service_name",
            "teacher",
            "capacity",
            "schedule" 
        )

class ScheduleActivitiesSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source='service.name',read_only=True)
    teacher_name = serializers.CharField(source='teacher.person.name',read_only=True)
    schedule = ScheduleSerializer(many=False)
    class Meta:
        model = Activity
        fields = (
            # "id",
            "dayofweek",
            # "dayofmonth",
            "startime",
            "endtime",
            "service_name",
            "teacher_name", 
            "schedule",
        )
