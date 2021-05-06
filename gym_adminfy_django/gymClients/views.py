from django.shortcuts import render
from django.http import Http404
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Client
from .serializers import ClientSerializer, ClientStateSerializer

class AllClients(ListCreateAPIView):
    queryset = Client.objects.select_related()
    serializer_class = ClientSerializer
    