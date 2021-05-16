from django.shortcuts import render
from django.http import Http404

from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from django.contrib.auth.models import User

from rest_framework import status, authentication, permissions

class GetPermissionsByUser(ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, format=None):
        permission = User.objects.get(pk = request.user.id).get_all_permissions()
        return Response(permission)