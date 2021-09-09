from django.contrib import admin

# Register your models here.
from .models import Person,Userofperson

admin.site.register(Person)
admin.site.register(Userofperson)