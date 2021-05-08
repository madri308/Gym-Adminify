from django.db import models
from django.contrib.auth.models import Permission
from django.contrib import admin


class PermissionAdmin(admin.ModelAdmin):
    model = Permission
    fields = ['name','content_type','codename']