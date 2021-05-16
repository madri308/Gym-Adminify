from django.shortcuts import render
from rest_framework import serializers

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics

from .serializers import ActivitiesSerializer,ScheduleActivitiesSerializer
#, ActivityHasClientSerializer
#from gymClients.serializers import ClientSerializer

from .models import Activity,Client

class AllActivities(generics.ListCreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitiesSerializer

class AllScheduleActivities(generics.ListCreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ScheduleActivitiesSerializer
