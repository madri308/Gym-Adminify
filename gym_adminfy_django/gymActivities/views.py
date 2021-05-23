from django.shortcuts import render
from rest_framework import serializers

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status

from .serializers import ActivitiesSerializer,ScheduleActivitiesSerializer
#, ActivityHasClientSerializer
#from gymClients.serializers import ClientSerializer

from .models import Activity,Client

class AllActivities(ListCreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitiesSerializer

class AllScheduleActivities(ListCreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ScheduleActivitiesSerializer

class ActivityDetail(RetrieveUpdateDestroyAPIView):
    model = Activity
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return ActivitiesSerializer
        return ActivitiesSerializer
    def get(self, request, *args, **kwargs):
        activity = Activity.objects.get(pk=kwargs['activity_id'])
        serializer = ActivitiesSerializer(activity)
        return Response(serializer.data)
    def delete(self, request, activity_id, format=None):
        activity = Activity.objects.get(pk=activity_id)
        activity.delete()
        return Response(status=status.HTTP_200_OK)
    