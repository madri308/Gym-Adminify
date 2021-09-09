from django.db import models

class Service(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=45)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=80)  # Field name made lowercase.      
    hourfee = models.DecimalField(db_column='HourFee', max_digits=15, decimal_places=2)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Service'

    def get_absolute_url(self):
        return f'/{self.id}/'
    def __str__(self):
        return self.name