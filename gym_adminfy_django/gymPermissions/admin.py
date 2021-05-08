from django.contrib import admin

from .models import AuthPermission, AuthGroupPermissions
# Register your models here.
admin.site.register(AuthPermission)
admin.site.register(AuthGroupPermissions)
