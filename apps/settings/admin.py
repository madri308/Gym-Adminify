from django.contrib import admin

# Register your models here.
from .models import Config,Room,Gym

admin.site.register(Config)
admin.site.register(Room)
admin.site.register(Gym)