from django.db import models

# from gymActivities.models import Activity
# from gymTeachers.models import Teacher
# from gymSettings.models import Config
# from gymPersons.models import Person
# from AdmSchedule.models import Schedule
# from gymServices.models import Service
# from .serializers import ActivitiesBUSerializer
from rest_framework import status, authentication, permissions
from rest_framework.generics import ListCreateAPIView

class ActivityBU(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    capacity = models.IntegerField(db_column='Capacity')  # Field name made lowercase.
    dayofweek = models.IntegerField(db_column='dayOfWeek')  # Field name made lowercase.
    dayofmonth = models.IntegerField(db_column='dayOfMonth')  # Field name made lowercase.
    startime = models.TimeField(db_column='StarTime')  # Field name made lowercase.
    endtime = models.TimeField(db_column='EndTime')  # Field name made lowercase.
    schedule = models.IntegerField(db_column='Schedule_ID')  # Field name made lowercase.
    service = models.IntegerField(db_column='Service_ID')  # Field name made lowercase.
    teacher = models.IntegerField(db_column='Teacher_ID')  # Field name made lowercase.
    creator = models.IntegerField(db_column='creator_ID')
    state = models.IntegerField(db_column='State')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Activity_backup'
    
    def get_absolute_url(self):
        return f'/{self.id}/'

    def addMemento(self, activity):
        new_Act = ActivityBU( id = activity.id,
                              capacity = activity.capacity, 

                              dayofweek = activity.dayofweek,
                              dayofmonth = activity.dayofmonth,

                              startime = activity.startime, 
                              endtime = activity.endtime,

                              service = activity.service.id, 
                              teacher = activity.teacher.person.id,
                              schedule = activity.schedule.id,

                              creator = activity.creator.id,
                              state = activity.state,
                            )
        new_Act.save()

    def restoreMemento(self, pID):
        return ActivityBU.objects.get(id=pID)


        # serviceBU = Service.objects.get(id=actBU.service)
        # teacherBU = Teacher.objects.get(person_id = actBU.teacher) 
        # scheduleBU = Schedule.objects.last()
        # teacherBU = Person.objects.get(id = actBU.creator) 
        
        # new_Act = Activity( id = actBU.id,
        #                     capacity = actBU.capacity, 

        #                     dayofweek = actBU.dayofweek,
        #                     dayofmonth = actBU.dayofmonth,

        #                     startime = actBU.startime, 
        #                     endtime = actBU.endtime,

        #                     service = serviceBU, 
        #                     teacher = teacherBU,
        #                     schedule = scheduleBU,

        #                     creator = actBU.creator.id,
        #                     state = actBU.state,
        #                    )
        
        # # Borra la actividad modificada que no fue aceptada
        # act = Activity.objects.get(id=pID)
        # act.delete()
        # # Guarda la nuev actividad
        # new_Act.save()
        # # Borra el backup existente
        # actBU.delete()


    