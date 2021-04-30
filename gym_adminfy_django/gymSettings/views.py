from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import ConfigSerializer

from .models import Config

class ConfigOne(APIView):
    def get(self, request, format=None):
        configs = Config.objects.all()
        serializer = ConfigSerializer(configs,many=True)
        return Response(serializer.data)