import datetime
from django.db import models
from gymPersons.models import Person
from gymClients.models import Client
#from gymActivity.models import Activity

# Create your models here.
class PayMethod(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PayMethod'

class Bill(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    paid = models.IntegerField(db_column='Paid')  # Field name made lowercase.
    paymentday = models.DateField(db_column='PaymentDay', blank=True, null=True)  # Field name made lowercase. 
    issuedate = models.DateField(db_column='IssueDate')  # Field name made lowercase.
    cost = models.DecimalField(db_column='Cost', max_digits=15, decimal_places=2)  # Field name made lowercase.
    #activity = models.ForeignKey(Activity, models.DO_NOTHING, db_column='Activity_ID')  # Field name made lowercase.
    paymethod = models.ForeignKey(PayMethod, models.DO_NOTHING, db_column='PayMethod_ID')  # Field name made lowercase.
    client = models.ForeignKey(Client, models.DO_NOTHING, db_column='Client_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Bill'

    def get_absolute_url(self):
        return f'/{self.id}/'

    def get_month(self):
        month = self.issuedate.month
        return month