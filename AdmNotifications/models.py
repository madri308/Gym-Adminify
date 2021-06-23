from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Notifications(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    message = models.CharField(db_column='Message', max_length=150)  
    user = models.ForeignKey(User,  on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'Notifications'
    def __str__(self):
        return self.message