from django.db import models

class Schedule(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    month = models.IntegerField(db_column='Month')  # Field name made lowercase.
    year = models.IntegerField(db_column='Year')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Schedule'
