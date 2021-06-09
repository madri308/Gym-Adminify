import calendar
from datetime import date, datetime
from collections import namedtuple

import json
from django.core.serializers.json import DjangoJSONEncoder


from django.shortcuts import render
from rest_framework import serializers

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from rest_framework import status, authentication, permissions

from .serializers import ActivitiesSerializer, ScheduleActivitiesSerializer,SpecificDataActivitiesSerializer,GeneralActivitiesSerializer
from gymServices.serializers import ServiceSerializer
from gymTeachers.serializers import TeacherSerializer
from gymSettings.serializers import ConfigSerializer, ConfigSerializerCapacity
from gymClients.serializers import ClientNameSerializer
from django.db.models import Count

from .models import Activity
from gymClients.models import Client, ClientState
from gymServices.models import Service
from gymTeachers.models import Teacher
from gymSettings.models import Config
from AdmSchedule.models import Schedule
from gymClients.models import Client
from AdmBills.models import Bill, PayMethod

class SpecificActivities(ListCreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitiesSerializer

    def get(self, request, *args, **kwargs):
        activity = Activity.objects.filter(startime=kwargs['startime'],dayofweek=kwargs['day']).only('dayofmonth','client','id')
        ser = SpecificDataActivitiesSerializer(activity, many=True)
        for act in ser.data:
            noMatriculados = Client.objects.exclude(pk__in=[o['person'] for o in act['client']])
            noMat_ser = ClientNameSerializer(noMatriculados,many=True)
            act['unrolled_clients'] = noMat_ser.data
        return Response(ser.data,status=status.HTTP_202_ACCEPTED)

class AllActivities(ListCreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitiesSerializer

    def get(self, request, *args, **kwargs):
        config = Config.objects.last()
        config_ser = ConfigSerializerCapacity(config, many=False)
        todays_date = date.today()
        m = todays_date.month
        y = todays_date.year
        general_activities = Activity.objects.raw('SELECT 1 as ID, Capacity,EndTime,Schedule_ID,Service_ID,Teacher_ID,dayOfWeek,StarTime,COUNT(dayOfWeek) AS "a",COUNT(StarTime) as "b" FROM Activity INNER JOIN Schedule ON Schedule.ID = Schedule_ID WHERE Schedule.Year ='+ str(y) +' AND Schedule.Month ='+ str(m) +' GROUP BY Capacity,Schedule_ID,dayOfWeek,StarTime,EndTime,Service_ID,Teacher_ID')
        gen_act_ser = GeneralActivitiesSerializer(general_activities,many=True)
    
        return Response({'config':config_ser.data, 'gen_act':gen_act_ser.data},status=status.HTTP_202_ACCEPTED)
    
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
        service = Service.objects.get(name=activity.service)
        clients_enroll = request.data['clientsToEnroll']
        clients_unenroll = request.data['clientsToUnenroll']
        today = datetime.today()
        duration = (activity.endtime.hour - activity.startime.hour)
        activities_related = Activity.objects.all().filter(dayofweek = activity.dayofweek, startime = activity.startime) 
        not_paid = PayMethod.objects.get(name = "Sin Pagar")

        for act in activities_related:
            for element in clients_enroll:
                client = Client.objects.get(person_id=element)
                if (client.clientstate.name == "Activo"):
                    act.client.add(client)
                    b = Bill(
                        paid = 0,
                        paymentday = None,
                        issuedate = today.strftime("%Y-%m-%d"),
                        cost = service.hourfee * duration,
                        activity = act,
                        paymethod = not_paid,
                        client = client
                    )
                    b.save()
                # se necesita crear la factura
            for element in clients_unenroll:
                client = Client.objects.get(person_id=element)
                act.client.remove(client)
                # borrar la actura
                bill = Bill.objects.get(activity = act.id,client = client.person.id) 
                if (act.dayofmonth - today.day) > 0 or (activity.startime.hour - today.hour) >= 8:
                    # si tiene balance
                    if (bill.paid == 1):
                        client.balance += bill.cost
                        client.save(update_fields=["balance"])
                bill.delete()
            act.save()
        return Response(status=status.HTTP_202_ACCEPTED)

class AllScheduleActivities(ListCreateAPIView):
    queryset = Activity.objects.raw('SELECT 1 as ID, EndTime,Schedule_ID,Service_ID,Teacher_ID,dayOfWeek,StarTime,COUNT(dayOfWeek) AS "a",COUNT(StarTime) as "b" FROM Activity GROUP BY dayOfWeek,StarTime,EndTime,Schedule_ID,Service_ID,Teacher_ID')
    serializer_class = ScheduleActivitiesSerializer
    
class ActivityDetail(RetrieveUpdateDestroyAPIView):
    model = Activity
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return ActivitiesSerializer
        return ActivitiesSerializer

    services = Service.objects.all()
    config = Config.objects.last()
    def get(self, request, *args, **kwargs):
        service_ser = ServiceSerializer(self.services,many=True)
        config_ser = ConfigSerializer(self.config, many=False)
        return Response({'service':service_ser.data, "config":config_ser.data})

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
