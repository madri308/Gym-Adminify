from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import ConfigSerializer, GymSerializer, RoomSerializer

from .models import Config, Gym, Room

class OneConfig(APIView):
    def get_first_object(self):
        try:
            return Config.objects.first()
        except Config.DoesNotExist:
            raise Http404
    def get(self, request, format=None):
        config = self.get_first_object()
        serializer = ConfigSerializer(config,many=False)
        return Response(serializer.data)

class OneGym(APIView):
    def get_first_object(self):
        try:
            return Gym.objects.first()
        except Gym.DoesNotExist:
            raise Http404
    def get(self, request, format=None):
        gym = self.get_first_object()
        serializer = GymSerializer(gym,many=False)
        return Response(serializer.data)

class OneRoom(APIView):
    def get_first_object(self):
        try:
            return Room.objects.first()
        except Room.DoesNotExist:
            raise Http404
    def get(self, request, format=None):
        room = self.get_first_object()
        serializer = RoomSerializer(room,many=False)
        return Response(serializer.data)