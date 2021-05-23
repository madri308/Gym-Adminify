from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from .models import Schedule
from .serializers import ScheduleSerializer
from rest_framework.response import Response
from rest_framework import status

class AllSchedules(ListCreateAPIView):
    model = Schedule
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    def create(self, request, pk=None):
        if Schedule.objects.filter(month=request.data['month'], year=request.data['year']).exists():
            return Response(status=status.HTTP_302_FOUND)
        schedule = ScheduleSerializer(data=request.data)
        if not schedule.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        schedule.save()
        return Response(schedule.data,status=status.HTTP_201_CREATED)
       

class ScheduleDetails(ListCreateAPIView):
    model = Schedule
    serializer_class = ScheduleSerializer
    def get(self, request, *args, **kwargs):
        schedule = Schedule.objects.get(pk = kwargs['schedule_id'])
        serializer = ScheduleSerializer(schedule)
        return Response(serializer.data)