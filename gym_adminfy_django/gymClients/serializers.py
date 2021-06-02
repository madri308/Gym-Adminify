from rest_framework import serializers
from .models import Client,ClientState
from gymPersons.serializers import PersonSerializer,PersonNameSerializer

class ClientSerializer(serializers.ModelSerializer):
    person = PersonSerializer(many=False)
    clientstate = serializers.CharField(read_only=True)
    class Meta:
        model = Client
        fields = (
            "person",
            "balance",
            "clientstate",
            "get_absolute_url"
        )

class ClientNameSerializer(serializers.ModelSerializer):
    person = PersonNameSerializer(many=False)
    class Meta:
        model = Client
        fields = (
            "person",
        )

class ClientStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientState

class NewClientSerializer(serializers.ModelSerializer):
    person = PersonSerializer(many=False)
    clientstate = serializers.CharField(read_only=True)
    class Meta:
        model = Client
        fields = (
            "person",
            "balance",
            "clientstate",
        )

