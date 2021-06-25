from django.db import models

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

    