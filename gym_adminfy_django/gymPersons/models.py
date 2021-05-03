from django.db import models

class Person(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True) 
    name = models.CharField(max_length=45)
    phone = models.IntegerField()
    mail = models.CharField(max_length=45, db_collation='utf8_general_ci')

    class Meta:
        managed = False
        db_table = 'Person'
