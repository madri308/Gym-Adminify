from django.db import models

from gymClients.models import Client
from gymServices.models import Service
from gymTeachers.models import Teacher
from AdmSchedule.models import Schedule

class Activity(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    capacity = models.IntegerField(db_column='Capacity')  # Field name made lowercase.
    dayofweek = models.IntegerField(db_column='dayOfWeek')  # Field name made lowercase.
    startime = models.TimeField(db_column='StarTime')  # Field name made lowercase.
    endtime = models.TimeField(db_column='EndTime')  # Field name made lowercase.
    schedule = models.ForeignKey('AdmSchedule.Schedule', models.DO_NOTHING,related_name='schedule' ,db_column='Schedule_ID')  # Field name made lowercase.
    service = models.ForeignKey('gymServices.Service', models.DO_NOTHING, db_column='Service_ID')  # Field name made lowercase.
    teacher = models.ForeignKey('gymTeachers.Teacher', models.DO_NOTHING, db_column='Teacher_ID')  # Field name made lowercase.
    client = models.ManyToManyField(Client)

    class Meta:
        managed = False
        db_table = 'Activity'
    def __str__(self):
        return f'{self.service.name} - {self.teacher.person.name} - {self.dayofweek}/{self.schedule.month}/{self.schedule.year}'

# class ActivityHasClient(models.Model):
#     id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
#     activity = models.ForeignKey(Activity, models.DO_NOTHING, db_column='Activity_ID')  # Field name made lowercase.
#     client = models.ForeignKey('gymClients.Client', models.DO_NOTHING, db_column='Client_ID')  # Field name made lowercase.
    
#     class Meta:
#         managed = False
#         db_table = 'Activity_has_Client'

