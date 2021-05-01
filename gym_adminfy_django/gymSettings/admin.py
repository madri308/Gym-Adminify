from django.contrib import admin

from .models import Config, Room, Gym 

admin.site.register(Config)
admin.site.register(Room)
admin.site.register(Gym)