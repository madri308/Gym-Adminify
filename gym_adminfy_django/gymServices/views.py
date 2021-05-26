from .models import Service
from rest_framework import status
from .serializers import ServiceSerializer
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView



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
    
    def put(self, request , service_id,*args, **kwargs):
        service = Service.objects.get(id=service_id)
        service_data = request.data
        service_serializer = ServiceSerializer(service, data=service_data)
        if not service_serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        service_serializer.save()
        return Response(status=status.HTTP_200_OK)
