import calendar
from datetime import date, datetime
from typing import Any
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import status, authentication, permissions
from .serializers import ActivitiesSerializer, ScheduleActivitiesSerializer,SpecificDataActivitiesSerializer,GeneralActivitiesSerializer
from gymServices.serializers import ServiceSerializer
from gymSettings.serializers import ConfigSerializer, ConfigSerializerCapacity
from gymClients.serializers import ClientNameSerializer
from .models import Activity
from gymActivitiesBU.models import ActivityBU
from gymServices.models import Service
from gymTeachers.models import Teacher
from gymSettings.models import Config
from AdmSchedule.models import Schedule
from gymClients.models import Client
from AdmBills.models import Bill, PayMethod
from gymPersons.models import Userofperson, Person
from django.db import transaction
from django.contrib.auth.models import User

class AllScheduleActivities(ListCreateAPIView):    
    queryset = Activity.objects.raw('SELECT 1 as ID, EndTime,Schedule_ID,Service_ID,Teacher_ID,dayOfWeek,StarTime,COUNT(dayOfWeek) AS "a",COUNT(StarTime) as "b" FROM Activity GROUP BY dayOfWeek,StarTime,EndTime,Schedule_ID,Service_ID,Teacher_ID')
    serializer_class = ScheduleActivitiesSerializer

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

class Visitor():
    def __init__(self):
        self.queryString  = ""
        self.rawObjects = Any
        self.todays_date = date.today()
        self.m = self.todays_date.month
        self.y = self.todays_date.year

    def getActivities(self, user):
        if user.groups.filter(name = "Teacher"): 
            return self.visitTeacher(user.id)
        elif user.groups.filter(name = "Clients"):
            return self.visitClient()
        return self.visitAdmin()

    def visitTeacher(self,  idPerson):
        self.queryString = 'SELECT 1 as ID, creator_ID,State,Capacity,EndTime,Schedule_ID,Service_ID,Teacher_ID,dayOfWeek,StarTime,COUNT(dayOfWeek) AS "a",COUNT(StarTime) as "b" FROM Activity INNER JOIN Schedule ON Schedule.ID = Schedule_ID WHERE Schedule.Year ='+ str(self.y) +' AND Schedule.Month ='+ str(self.m) +' AND (Activity.creator_ID ='+ str(idPerson)+ ' OR Activity.Teacher_ID ='+ str(idPerson)+') GROUP BY creator_ID,State,Capacity,Schedule_ID,dayOfWeek,StarTime,EndTime,Service_ID,Teacher_ID'
        return Activity.objects.raw(self.queryString)

    def visitAdmin(self):
        self.queryString = 'SELECT 1 as ID, creator_ID,State,Capacity,EndTime,Schedule_ID,Service_ID,Teacher_ID,dayOfWeek,StarTime,COUNT(dayOfWeek) AS "a",COUNT(StarTime) as "b" FROM Activity INNER JOIN Schedule ON Schedule.ID = Schedule_ID WHERE Schedule.Year ='+ str(self.y) +' AND Schedule.Month ='+ str(self.m) +' GROUP BY creator_ID,State,Capacity,Schedule_ID,dayOfWeek,StarTime,EndTime,Service_ID,Teacher_ID'
        return Activity.objects.raw(self.queryString)

    def visitClient(self):
        self.queryString = 'SELECT 1 as ID, creator_ID,State,Capacity,EndTime,Schedule_ID,Service_ID,Teacher_ID,dayOfWeek,StarTime,COUNT(dayOfWeek) AS "a",COUNT(StarTime) as "b" FROM Activity INNER JOIN Schedule ON Schedule.ID = Schedule_ID WHERE Schedule.Year ='+ str(self.y) +' AND Schedule.Month ='+ str(self.m) +' AND Activity.State = 1 GROUP BY creator_ID,State,Capacity,Schedule_ID,dayOfWeek,StarTime,EndTime,Service_ID,Teacher_ID'
        return Activity.objects.raw(self.queryString)

class AllActivities(ListCreateAPIView):
    visitor = Visitor()
    queryset = Activity.objects.all()
    serializer_class = ActivitiesSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk = request.user.id)
        config = Config.objects.last()
        config_ser = ConfigSerializerCapacity(config, many=False)
        general_activities = self.visitor.getActivities(user) 
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

    @transaction.atomic
    def createByTeacher(self,request,user):
        selected_service = Service.objects.get(id=request.data['service'])
        selected_teacher = Teacher.objects.get(person_id = Userofperson.objects.get(user = request.user.id).person) 
        selected_schedule = Schedule.objects.last() 
        new_Act = None
        superusers = User.objects.filter(is_superuser=True).first()
        for element in self.getDatesByDay(request.data['day'],selected_schedule.month,selected_schedule.year):
            new_Act = Activity( capacity = request.data['service'], 
                                dayofweek = request.data['day'],
                                dayofmonth = element.day,

                                startime = request.data['startTime'], 
                                endtime = request.data['endTime'],

                                service = selected_service, 
                                teacher = selected_teacher,
                                schedule = selected_schedule,

                                creator = user,
                                state = 0,                    
                            )
            new_Act.save()
            # OBSERVER
            new_Act.attach(superusers)
            new_Act.attach(user)
        new_Act.notify("Solicitud de "+user.username+": creacion de la actividad "+new_Act.service.name)
        
    def createByAdmin(self,request, user):
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
                                schedule = selected_schedule,

                                creator = user,
                                state = 1,                    
                            )
            new_Act.attach(user)
            new_Act.save()

    def create(self, request, pk=None):
        if self.checkOverlap(request.data['startTime'],request.data['endTime'], request.data['day']):
            return Response(status=status.HTTP_409_CONFLICT)
        user = User.objects.get(pk = request.user.id)
        createActivities = self.createByTeacher if user.groups.filter(name = "Teacher") else self.createByAdmin
        createActivities(request, user)
            
        return Response(status=status.HTTP_202_ACCEPTED)

class ActivityEnrollClients(ListCreateAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitiesSerializer

    @transaction.atomic
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
                if (client.clientstate.name != "Activo"):
                    content = {'Error': 'Hay un cliente moroso'}
                    return Response(content,status=status.HTTP_406_NOT_ACCEPTABLE)
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



    
class ActivityDetail(RetrieveUpdateDestroyAPIView):
    model = Activity
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return ActivitiesSerializer
        return ActivitiesSerializer

    services = Service.objects.all()
    def get(self, request, *args, **kwargs):
        service_ser = ServiceSerializer(self.services,many=True)
        return Response({'service':service_ser.data})

    def delete(self, request, activity_id, format=None):
        activity = Activity.objects.get(pk=activity_id)
        activity.delete()
        
        return Response(status=status.HTTP_200_OK)

    def put(self, request, **kwargs):
        user = User.objects.get(pk = request.user.id)
        print(user)
        putActivities = self.putByTeacher if user.groups.filter(name = "Teacher") else self.putByAdmin
        putActivities(request, **kwargs)
            
        return Response(status=status.HTTP_202_ACCEPTED)

    def putByAdmin(self, request, **kwargs):
        activity = Activity.objects.get(id=kwargs['activity_id'])
        activities_related = Activity.objects.all().filter(dayofweek = activity.dayofweek, 
                                                            startime = activity.startime) 
        for act in activities_related:
            act.capacity = request.data['capacity']
            act.dayofweek = request.data['dayofweek']
            act.startime = request.data['startime']
            act.endtime = request.data['endtime']
            act.save(update_fields=['capacity','dayofweek', 'startime','endtime'])

    def putByTeacher(self, request, **kwargs):
        activity = Activity.objects.get(id=kwargs['activity_id'])
        activityBU = ActivityBU( id = activity.id)
        activityBU.addMemento(activity)
        activities_related = Activity.objects.all().filter(dayofweek = activity.dayofweek, 
                                                            startime = activity.startime) 
        for act in activities_related:
            act.capacity = request.data['capacity']
            act.dayofweek = request.data['dayofweek']
            act.startime = request.data['startime']
            act.endtime = request.data['endtime']
            act.state = 0
            act.save(update_fields=['capacity','dayofweek', 'startime','endtime', 'state'])        

class ActivityRejected(RetrieveUpdateDestroyAPIView):
    model = Activity
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return ActivitiesSerializer
        return ActivitiesSerializer

    @transaction.atomic
    def put(self, request, *args, **kwargs):
        activity = Activity.objects.get(id=kwargs['activity_id'])
        activities_related = Activity.objects.all().filter(dayofweek = activity.dayofweek, 
                                                            startime = activity.startime) 
        
        # Volver al estado original
        backUp = ActivityBU.objects.filter(id = activity.id)
        if backUp.count() > 0: #encuentra un back up, lo restaura
            actBU = backUp[0].restoreMemento(backUp[0].id)
            # serviceBU = Service.objects.get(id=actBU.service)
            # teacherBU = Teacher.objects.get(person_id = actBU.teacher) 
            # scheduleBU = Schedule.objects.last()
            # userBU = User.objects.get(id = actBU.creator)
            for act in activities_related:
                act.capacity = actBU.capacity
                act.dayofweek = actBU.dayofweek
                act.startime = actBU.startime
                act.endtime = actBU.endtime
                act.state = 1
                act.save(update_fields=["capacity","dayofweek","startime","endtime","state"])
                #borra la copia ya restaurada
            activity.notify("El administrador ha rechazado la solicitud de modificación a "+activity.service.name)
            backUp.delete()
        else:
            activity.notify("El administrador ha rechazado tu solicitud de creación de "+activity.service.name)
            activity.detachAll()
            activity.delete()
        return Response(status=status.HTTP_200_OK)

class ActivityAccepted(RetrieveUpdateDestroyAPIView):
    model = Activity
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return ActivitiesSerializer
        return ActivitiesSerializer

    @transaction.atomic
    def put(self, request, *args, **kwargs):
        activity = Activity.objects.get(id=kwargs['activity_id'])
        activities_related = Activity.objects.all().filter(dayofweek = activity.dayofweek, 
                                                            startime = activity.startime) 
        
        activityBU = ActivityBU.objects.filter(id=kwargs['activity_id'])
        if activityBU.count() > 0:
            activityBU.delete()

        for act in activities_related:
            act.state = 1
            act.save(update_fields=['state'])
        act.notify("El administrador ha aceptado tu actividad de "+act.service.name)
        return Response(status=status.HTTP_200_OK)

class ActivityTeacher(RetrieveUpdateDestroyAPIView):
    model = Activity
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return ActivitiesSerializer
        return ActivitiesSerializer

    def put(self, request, *args, **kwargs):
        activity = Activity.objects.get(id=kwargs['activity_id'])
        teacher = Teacher.objects.get(person_id=request.data['teacher'])
        activity.teacher = teacher
        activity.save(update_fields=["teacher"])
        return Response(activity.teacher.person.name,status=status.HTTP_202_ACCEPTED)