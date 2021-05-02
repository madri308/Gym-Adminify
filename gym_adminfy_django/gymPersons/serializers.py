from rest_framework import serializers

from .models import Person

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = (
            "id",
            "teachercategory",
            "name",
            "phone",
            "mail",
            "get_absolute_url"
        )