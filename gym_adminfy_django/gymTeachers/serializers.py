from rest_framework import serializers
from .models import Teacher,Teachercategory
from gymPersons.serializers import PersonSerializer

class TeacherSerializer(serializers.ModelSerializer):
    person = PersonSerializer(many=False)
    category_name = serializers.CharField(source='teachercategory.name',read_only=True)
    class Meta:
        model = Teacher
        fields = (
            "person",
            "category_name",
            "get_absolute_url"
        )

class TeachercategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Teachercategory

class TeacherNamesSerializer(serializers.ModelSerializer):
    person = PersonSerializer(many=False)
    class Meta:
        model = Teacher
        fields = (
            "person",
            "category_name",
            "get_absolute_url"
        )