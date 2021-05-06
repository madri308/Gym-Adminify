from django.contrib import admin

from .models import Client, ClientState
# Register your models here.
admin.site.register(Client)
admin.site.register(ClientState)


