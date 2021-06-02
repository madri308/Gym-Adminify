from rest_framework import serializers

from .models import Person,Userofperson

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