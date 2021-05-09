from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import ActivitiesSerializer, ActivityHasClientSerializer
from gymClients.serializers import ClientSerializer

from .models import Activity, ActivityHasClient, Client

# Queries
class AllActivities(APIView):
    def get(self, request, format=None):
        activities = Activity.objects.all()
        serializer = ActivitiesSerializer(activities, many=True)
        return Response(serializer.data)

class AllClientsByActivity(APIView):
    def get(self, request, activity_id, format=None):
        clients = ActivityHasClient.objects.all().filter(activity=activity_id)
        serializer = ClientSerializer(clients,many=True)
        return Response(serializer.data)

# class GetAll(APIView):
#     def get(self, request, format=None):
#         activities = Activity.objects.all()
#         match = ActivityHasClient.objects.all()
#         clients = Client.objects.all()
#         serializerAct = ActivitiesSerializer(activities, many=True)
#         serializerMatch = ActivityHasClientSerializer(match, many=True)
#         serializerClient = ClientSerializer(clients,many=True)

#         return Response(serializerAct.data, serializerMatch.data, serializerClient.data)