from rest_framework import serializers
from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Person,Userofperson

class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = (
            "id",
            "name",
            "phone",
            "mail",
            "identification"
        )

class PersonNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = (
            "id",
            "name"
        )

class UserofpersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userofperson
        fields = (
            "id",
            "person",
            "user"
        )