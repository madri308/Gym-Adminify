from django.shortcuts import render
from django.http import Http404
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import AuthPermission, AuthGroupPermissions
from .serializers import AuthPermissionSerializer, AuthGroupPermissionSerializer

class AllPermissionsGroup(ListCreateAPIView):
    def get(self, request, category_id, format=None):
        permissions = AuthPermission.objects.all().filter(group=category_id)
        serializer = AuthPermission(permissions)
        return Response(serializer.data)