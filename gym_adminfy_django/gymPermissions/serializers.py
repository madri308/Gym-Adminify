from rest_framework import serializers
from .models import AuthPermission, AuthGroupPermissions
from django.contrib.auth.models import User

class AuthPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthPermission
        fields = (
            "name",
            "content_type",
            "codename",
        )

class AuthGroupPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthGroupPermissions
        fields = (
            "id", 
            "group",
            "permission"
        )

class UserSerializer(serializers.ModelSerializer):
    user_permissions = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id', 'username', 'user_permissions')
    def get_user_permissions(self, obj):
        return list(obj.user_permissions.all())
