from rest_framework import serializers

from .models import Person

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = (
            "id",
            "name",
            "phone",
            "mail"
        )

class PersonNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = (
            "id",
            "name"
        )
