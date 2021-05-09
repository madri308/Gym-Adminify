from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render

from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth.decorators import permission_required

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
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_first_object(self):
        try:
            return Gym.objects.first()
        except Gym.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        if request.user.has_perm('gymSettings.view_gym'):
            gym = self.get_first_object()
            serializer = GymSerializer(gym,many=False)
            return Response(serializer.data)
        else:
            raise Http404

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