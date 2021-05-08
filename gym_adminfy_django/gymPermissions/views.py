from django.shortcuts import render
from django.http import Http404

from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required

from .models import AuthPermission, AuthGroupPermissions
from .serializers import AuthPermissionSerializer, AuthGroupPermissionSerializer

class GetPermissionsByUser(ListCreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_id = request.user.username
        user = User.objects.get(pk=user_id)
        
        serializer = UserSerializer(user2.get_all_permissions())

        return Response(serializer.data)