from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render

from rest_framework import status, authentication, permissions
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView, UpdateAPIView

from .serializers import ConfigSerializer, GymSerializer, RoomSerializer
from .models import Config, Gym, Room

class OneConfig(RetrieveUpdateDestroyAPIView):
    model = Config
    serializer_class = ConfigSerializer

    def get_object(self):
        return Config.objects.first()

class OneGym(RetrieveUpdateDestroyAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    model = Gym
    serializer_class = GymSerializer

    def get_object(self):
        if self.request.user.has_perm('gymSettings.view_gym'):
            return Gym.objects.first()
        else:
            raise Http404

class OneRoom(RetrieveUpdateDestroyAPIView):
    model = Room
    serializer_class = RoomSerializer
    
    def get_object(self):
        return Room.objects.first()

class AllSettings(APIView):
    config = Config.objects.first()
    room = Room.objects.first()
    gym = Gym.objects.first()
    def get(self, request, *args, **kwargs):
        config_ser = ConfigSerializer(self.config, many=False)
        room_ser = RoomSerializer(self.room,many=False)
        gym_ser = GymSerializer(self.gym,many=False)
        return Response({"config":config_ser.data, 'room':room_ser.data, 'gym':gym_ser.data})

    def put(self, request, *args, **kwargs):
        config_ser = ConfigSerializer(instance=self.config, data=request.data['config'])
        # room_ser = RoomSerializer(instance=self.room, data=request.data['room'])
        gym_ser = GymSerializer(instance=self.gym, data=request.data['gym'])

        if not gym_ser.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if not config_ser.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # if not room_ser.is_valid():
        #     print(room_ser.errors)
        #     return Response(status=status.HTTP_400_BAD_REQUEST)

        config_ser.save()
        gym_ser.save()
        # room_ser.save()
        return Response(status=status.HTTP_202_ACCEPTED)