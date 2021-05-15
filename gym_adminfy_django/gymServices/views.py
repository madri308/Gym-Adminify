from django.shortcuts import render

from .models import Service
from .serializers import ServiceSerializer

from rest_framework import status
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView

from rest_framework.response import Response



# Queries
class AllServices(ListCreateAPIView):
    model = Service
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ServiceSerializer
        return ServiceSerializer

    def get_queryset(self):
        return Service.objects.all()

class ServiceDetail(RetrieveUpdateDestroyAPIView):
    model = Service
    queryset = Service.objects.all()
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ServiceSerializer
        return ServiceSerializer
    
    def get(self, request, *args, **kwargs):
        service = Service.objects.get(id=kwargs['service_id'])
        serializer = ServiceSerializer(service)
        return Response(serializer.data)

    def delete(self, request, service_id, format=None):
        service = Service.objects.get(id=service_id)
        service.delete()
        return Response(status=status.HTTP_200_OK)
