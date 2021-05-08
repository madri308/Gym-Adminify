from rest_framework import serializers
from .models import AuthPermission, AuthGroupPermissions

class AuthPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthPermission
        fields = (
            "name",
            "content_type",
            "codename",

class AuthGroupPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthGroupPermissions
        fields = (
            "id", 
            "group",
            "permission"
        )

