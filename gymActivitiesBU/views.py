from django.shortcuts import render

from .models import ActivityBU
from gymActivities.models import Activity
from gymTeachers.models import Teacher
from gymSettings.models import Config
from gymPersons.models import Person
from AdmSchedule.models import Schedule
from gymServices.models import Service
from .serializers import ActivitiesBUSerializer
from rest_framework import status, authentication, permissions
from rest_framework.generics import ListCreateAPIView

# Create your views here.

class AllActivities(ListCreateAPIView):
    queryset = ActivityBU.objects.all()
    serializer_class = ActivitiesBUSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def addMemento(self, activity):
        new_Act = ActivityBU( id = activity.id,
                              capacity = activity.capacity, 

                              dayofweek = activity.dayofweek,
                              dayofmonth = activity.dayofmonth,

                              startime = activity.startime, 
                              endtime = activity.endtime,

                              service = activity.service.id, 
                              teacher = activity.teacher.id,
                              schedule = activity.schedule.id,

                              creator = activity.creator.id,
                              state = activity.state,
                            )
        new_Act.save()

    def restoreMemento(self, pID):
        actBU = ActivityBU.objects.get(id=pID)

        serviceBU = Service.objects.get(id=actBU.service)
        teacherBU = Teacher.objects.get(person_id = actBU.teacher) 
        scheduleBU = Schedule.objects.last()
        teacherBU = Person.objects.get(id = actBU.creator) 
        
        new_Act = Activity( id = actBU.id,
                            capacity = actBU.capacity, 

                            dayofweek = actBU.dayofweek,
                            dayofmonth = actBU.dayofmonth,

                            startime = actBU.startime, 
                            endtime = actBU.endtime,

                            service = serviceBU, 
                            teacher = teacherBU,
                            schedule = scheduleBU,

                            creator = actBU.creator.id,
                            state = actBU.state,
                           )
        
        # Borra la actividad modificada que no fue aceptada
        act = Activity.objects.get(id=pID)
        act.delete()
        # Guarda la nuev actividad
        new_Act.save()
        # Borra el backup existente
        actBU.delete()
