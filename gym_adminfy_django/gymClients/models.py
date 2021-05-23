from django.db import models
from gymPersons.models import Person

class Client(models.Model):
    person = models.OneToOneField(Person, models.DO_NOTHING, db_column='ID', primary_key=True)  # Field name made lowercase.
    balance = models.DecimalField(db_column='Balance', max_digits=15, decimal_places=2)  # Field name made lowercase.
    clientstate = models.ForeignKey('ClientState', models.DO_NOTHING, db_column='ClientState_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Client'
    def __str__(self):
        return self.person.name
    def get_absolute_url(self):
        return f'/{self.person.id}/'

class ClientState(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ClientState'

    def __str__(self):
        return self.name
        
    def get_absolute_url(self):
        return f'/{self.id}/'