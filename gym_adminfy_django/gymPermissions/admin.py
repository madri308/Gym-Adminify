from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import PermissionAdmin


admin.site.register(Permission, PermissionAdmin)
