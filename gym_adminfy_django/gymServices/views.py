from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import ServiceSerializer

from .models import Service


class ServiceOne(APIView):
    def get(self, request, format=None):
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)