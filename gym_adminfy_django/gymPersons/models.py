from django.db import models
from django.contrib.auth.models import User

class Person(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True) 
    name = models.CharField(max_length=45)
    phone = models.IntegerField()
    mail = models.CharField(max_length=45, db_collation='utf8_general_ci')
    identification = models.CharField(max_length=45)
    class Meta:
        managed = False
        db_table = 'Person'
    def __str__(self):
        return self.name

class Userofperson(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    person = models.OneToOneField('Person', models.DO_NOTHING, db_column='Person_ID')  # Field name made lowercase.
    user = models.ForeignKey(User, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'UserOfPerson'