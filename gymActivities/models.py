from django.db import models
from django.contrib.auth.models import User

from gymClients.models import Client

class Subject:
    _observers = []

    def attach(self, observer):
        if not observer in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self):
        for observer in self._observers:
            print("Notifico")


class Activity(models.Model,Subject):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    capacity = models.IntegerField(db_column='Capacity')  # Field name made lowercase.
    dayofweek = models.IntegerField(db_column='dayOfWeek')  # Field name made lowercase.
    dayofmonth = models.IntegerField(db_column='dayOfMonth')  # Field name made lowercase.
    startime = models.TimeField(db_column='StarTime')  # Field name made lowercase.
    endtime = models.TimeField(db_column='EndTime')  # Field name made lowercase.
    schedule = models.ForeignKey('AdmSchedule.Schedule', models.DO_NOTHING,related_name='schedule' ,db_column='Schedule_ID')  # Field name made lowercase.
    service = models.ForeignKey('gymServices.Service', models.DO_NOTHING, db_column='Service_ID')  # Field name made lowercase.
    teacher = models.ForeignKey('gymTeachers.Teacher', models.DO_NOTHING, db_column='Teacher_ID')  # Field name made lowercase.
    client = models.ManyToManyField(Client)
    creator = models.ForeignKey(User,  on_delete=models.CASCADE)
    state = models.IntegerField(db_column='State')  # Field name made lowercase.
    _observers = []  #reset observers
    # def __init__(self):
        
    class Meta:
        managed = False
        db_table = 'Activity'
    
    def get_absolute_url(self):
        return f'/{self.id}/'

    def __str__(self):
        return self.activity.service