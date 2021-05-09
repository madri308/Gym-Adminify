from django.db import models
from gymPersons.models import Person

class Teacher(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE, db_column='ID', primary_key=True)  
    teachercategory = models.ForeignKey('Teachercategory', on_delete=models.CASCADE, db_column='TeacherCategory_ID') 

    class Meta:
        managed = False
        db_table = 'Teacher'
        
    def get_absolute_url(self):
        return f'/{self.person.id}/'
    def __str__(self):
        return self.person.name

class Teachercategory(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True) 
    name = models.CharField(db_column='Name', max_length=45) 
    def __str__(self):
        return self.name
    class Meta:
        managed = False
        db_table = 'TeacherCategory'
    def get_absolute_url(self):
        return f'/{self.id}/'
