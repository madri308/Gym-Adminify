from rest_framework import serializers
from .models import Teacher,Teachercategory
from gymPersons.serializers import PersonSerializer
from gymServices.serializers import ServiceSerializer,NameServiceSerializer

class TeacherSerializer(serializers.ModelSerializer):
    person = PersonSerializer(many=False)
    services = NameServiceSerializer(many=True)
    class Meta:
        model = Teacher
        fields = (
            "person",
            "teachercategory",
            "get_absolute_url",
            "services"
        )

class NewTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = (
            "person",
            "teachercategory",
            "services"
        )

class TeachercategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Teachercategory
        fields = (
            "name",
            "get_absolute_url",
            "id"
        )

class TeacherNamesSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='person.name',read_only=True)
    class Meta:
        model = Teacher
        fields = (
            "name",
            "get_absolute_url"
        )