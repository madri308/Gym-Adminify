from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import activate

from gymClients.models import Client
from AdmNotifications.models import Notifications
class Activity(models.Model):
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

    def get_observers(self):
        return ActivityObservers.objects.filter(activity=self.pk)
    class Meta:
        managed = False
        db_table = 'Activity'
    
    def get_absolute_url(self):
        return f'/{self.id}/'

    def __str__(self):
        return self.activity.service

    def attach(self, observer):
        observers = self.get_observers()
        if not observer in observers:
            new_obs = ActivityObservers(activity = self, user = observer)
            new_obs.save()

    def detachAll(self):
        observers = self.get_observers()
        for observer in observers:
            observer.delete()

    def detach(self, observer):
        obs = ActivityObservers.objects.get(activity = self, user = observer)
        obs.delete()

    def notify(self, newMessage):
        observers = self.get_observers()
        for observer in observers:
            print(observer.user.id)
            new_msg = Notifications(message = newMessage, user = observer.user)
            new_msg.save()

class ActivityObservers(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    activity = models.ForeignKey('Activity', models.DO_NOTHING, db_column='activity_ID', blank=True, null=True)  # Field name made lowercase.
    user = models.ForeignKey(User,  on_delete=models.CASCADE)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Activity_observers'