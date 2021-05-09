from django.contrib import admin
from .models import Activity, ActivityHasClient

admin.site.register(Activity)
admin.site.register(ActivityHasClient)