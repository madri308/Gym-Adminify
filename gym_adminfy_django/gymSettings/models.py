from django.db import models

class Config(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    effectivedate = models.DateField(db_column='EffectiveDate')  # Field name made lowercase.
    capacitypercentage = models.DecimalField(db_column='CapacityPercentage', max_digits=5, decimal_places=4)  # Field name made lowercase.
    timeperday = models.JSONField(db_column='TimePerDay')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Config'
    def get_absolute_url(self):
        return f'/{self.id}/'
    def __str__(self):
        return f'{self.id} - {self.effectivedate}'

class Gym(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=45)  # Field name made lowercase.
    tuitioncost = models.DecimalField(db_column='TuitionCost', max_digits=15, decimal_places=2)  # Field name made lowercase.
    config = models.ForeignKey(Config, models.DO_NOTHING, db_column='Config_ID')  # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'Gym'
    def get_absolute_url(self):
        return f'/{self.id}/'
    def __str__(self):
        return f'{self.id} - {self.name}'

class Room(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=45)  # Field name made lowercase.
    capacity = models.IntegerField(db_column='Capacity')  # Field name made lowercase.
    gym = models.ForeignKey(Gym, models.DO_NOTHING, db_column='Gym_ID')  # Field name made lowercase.
    # schedule = models.ForeignKey('Schedule', models.DO_NOTHING, db_column='Schedule_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Room'
    def get_absolute_url(self):
        return f'/{self.id}/'
    def __str__(self):
        return f'{self.id} - {self.name}'