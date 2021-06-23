from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from .models import Notifications
from .serializers import NotificationsSerializer
from rest_framework import status, authentication, permissions

class AllNotifications(RetrieveUpdateDestroyAPIView):    
    model = Notifications
    queryset = Notifications.objects.all()
    serializer_class = NotificationsSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        notifications = Notifications.objects.filter(user=request.user.id)
        notif_ser = NotificationsSerializer(notifications,many=True)
        return Response(notif_ser.data,status=status.HTTP_202_ACCEPTED)
    def delete(self, request, format=None):
        Notifications.objects.filter(user=request.user.id).delete()
        return Response(status=status.HTTP_202_ACCEPTED)