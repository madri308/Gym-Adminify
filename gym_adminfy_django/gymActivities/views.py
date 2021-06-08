import calendar
from datetime import datetime
from collections import namedtuple

from django.shortcuts import render
from rest_framework import serializers

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status

from .serializers import ActivitiesSerializer, ScheduleActivitiesSerializer
from gymServices.serializers import ServiceSerializer
from gymTeachers.serializers import TeacherSerializer
from gymSettings.serializers import ConfigSerializer
from gymClients.serializers import ClientNameSerializer

from .models import Activity
from gymClients.models import Client, ClientState
from gymServices.models import Service
from gymTeachers.models import Teacher
from gymSettings.models import Config
from AdmSchedule.models import Schedule
from gymClients.models import Client

class AllActivities(ListCreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitiesSerializer

    Range = namedtuple('Range', ['start', 'end'])

    def get(self, request, *args, **kwargs):
        activities = Activity.objects.all()
        act_ser = ActivitiesSerializer(activities,many=True)
        
        for act in act_ser.data:
            noMatriculados = Client.objects.exclude(pk__in=[o['person'] for o in act['client']])
            noMat_ser = ClientNameSerializer(noMatriculados,many=True)
            act['unrolled_clients'] = noMat_ser.data
            act['newOnes'] = []
            act['deletedOnes'] = []
        return Response(act_ser.data,status=status.HTTP_202_ACCEPTED)
    
    def getDatesByDay(self, numberDay,month,year):
        c = calendar.Calendar(firstweekday=calendar.SUNDAY)
        monthcal = c.monthdatescalendar(year,month)
        dates = [day for week in monthcal for day in week if \
                    day.weekday() == numberDay-1 and \
                    day.month == month]
        return dates

    def checkOverlap(self,startTime,endTime, day):
        activities = Activity.objects.filter(dayofweek = day)
        for activity in activities:
            if activity.startime <= datetime.strptime(endTime, '%H:%M').time() and datetime.strptime(startTime, '%H:%M').time() <= activity.endtime:
                return True
        return False

    def create(self, request, pk=None):
        if self.checkOverlap(request.data['startTime'],request.data['endTime'], request.data['day']):
            return Response(status=status.HTTP_409_CONFLICT)
        selected_service = Service.objects.get(id=request.data['service'])
        selected_teacher = Teacher.objects.get(person_id=request.data['teacher'])
        selected_schedule = Schedule.objects.last()
        
        for element in self.getDatesByDay(request.data['day'],selected_schedule.month,selected_schedule.year):
            new_Act = Activity( capacity = request.data['service'], 
                                dayofweek = request.data['day'],
                                dayofmonth = element.day,

                                startime = request.data['startTime'], 
                                endtime = request.data['endTime'],

                                service = selected_service, 
                                teacher = selected_teacher,
                                schedule = selected_schedule                    
                            )
            new_Act.save()    
        return Response(status=status.HTTP_202_ACCEPTED)

class ActivityEnrollClients(ListCreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitiesSerializer

    def put(self, request, *args, **kwargs):
        activity = Activity.objects.get(id=kwargs['activity_id'])
        clients = request.data['clients']
        noMatriculados = Client.objects.exclude(pk__in=[o['person'] for o in act['client']])
        activities_related = Activity.objects.all().filter(dayofweek = activity.dayofweek, startime = activity.startime) 
        for act in activities_related:
            for element in clients:
                client = Client.objects.get(person_id=element)
                act.client.add(client)
            act.save()
        return Response(status=status.HTTP_202_ACCEPTED)

class ActivityUnenrollClients(ListCreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitiesSerializer

    def put(self, request, *args, **kwargs):
        activity = Activity.objects.get(id=kwargs['activity_id'])
        clients = request.data['clients']
        activities_related = Activity.objects.all().filter(dayofweek = activity.dayofweek, startime = activity.startime) 
        for act in activities_related:
            for element in clients:
                client = Client.objects.get(person_id=element)
                act.client.remove(client)
            act.save()
        return Response(status=status.HTTP_202_ACCEPTED)

class AllScheduleActivities(ListCreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ScheduleActivitiesSerializer

class ActivityDetail(RetrieveUpdateDestroyAPIView):
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
        activity = Activity.objects.get(id=kwargs['activity_id'])
        teacher = Teacher.objects.get(person_id=request.data['teacher'])

        activity.teacher = teacher

        activity.save(update_fields=["teacher"])
        return Response(status=status.HTTP_202_ACCEPTED)