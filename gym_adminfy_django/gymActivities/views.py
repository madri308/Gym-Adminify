from django.shortcuts import render
from rest_framework import serializers

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status#, authentication, permissions

from .serializers import ActivitiesSerializer
from gymServices.serializers import ServiceSerializer
from gymTeachers.serializers import TeacherSerializer
from gymSettings.serializers import ConfigSerializer

from .models import Activity
from gymServices.models import Service
from gymTeachers.models import Teacher
from gymSettings.models import Config


class AllActivities(generics.ListCreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitiesSerializer

class ActivityDetail(APIView):
    model = Activity
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return ActivitiesSerializer
        return ActivitiesSerializer

    services = Service.objects.all()
    teachers = Teacher.objects.all()
    config = Config.objects.first()
    def get(self, request, *args, **kwargs):
        service_ser = ServiceSerializer(self.services,many=True)
        teachers_ser = TeacherSerializer(self.teachers,many=True)
        config_ser = ConfigSerializer(self.config, many=False)
        
        return Response({'service':service_ser.data, 'teacher':teachers_ser.data, "config":config_ser.data})

    def delete(self, request, activity_id, format=None):
        activity = Activity.objects.get(pk=activity_id)
        activity.delete()
        return Response(status=status.HTTP_200_OK)


    def put(self, request, *args, **kwargs):
        obj, created = Activity.objects.update_or_create(
            defaults={'teacher': kwargs['teacher']},
        )
        return Response(status=status.HTTP_202_ACCEPTED)
