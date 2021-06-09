from django.contrib.auth.models import User
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from django.forms.models import model_to_dict
from .models import Client
from .serializers import ClientSerializer, ModifyClientSerializer, NewClientSerializer
from gymPersons.serializers import PersonSerializer,UserofpersonSerializer
from rest_framework import serializers, status
from django.db import transaction

class AllClients(ListCreateAPIView):
    model = Client
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NewClientSerializer
        return ClientSerializer

    def get_queryset(self):
        return Client.objects.all()
        
    @transaction.atomic
    def create(self, request, pk=None):
        # CREATE THE PERSON
        personSerializer = PersonSerializer(data=request.data)
        personSerializer.is_valid(raise_exception=True)
        personObject = personSerializer.save()
        # CREATE THE USER
        user = User.objects.create_user(request.data["mail"]
                                        ,request.data["mail"]
                                        ,request.data["identification"])
        user.save()
        user.groups.add(2)
        # CREATE RELATION
        userofpersonSerializer = UserofpersonSerializer(data={
                                            'person':personObject.pk,
                                            'user':user.pk })
                                        
        userofpersonSerializer.is_valid(raise_exception=True)
        userofpersonSerializer.save()
        # CREATE THE CLIENT
        serializer = NewClientSerializer(data={
                                            "person":personObject.pk,
                                            "clientstate": 4,
                                            "balance":0.00,
                                        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(personObject.pk, status=status.HTTP_201_CREATED)
            

class AllClientsByCategory(ListCreateAPIView):
    def get(self, request, category_id, format=None):
        clients = Client.objects.all().filter(teachercategory=category_id)
        serializer = ClientSerializer(clients,many=True)
        return Response(serializer.data)

class ClientDetail(RetrieveUpdateDestroyAPIView):    
    model = Client
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return NewClientSerializer
        return ClientSerializer

    def get(self, request, *args, **kwargs):
        teacher = Client.objects.get(person=kwargs['client_id'])
        serializer = ClientSerializer(teacher)
        return Response(serializer.data)

    def delete(self, request, client_id, format=None):
        teacher = Client.objects.get(person=client_id)
        teacher.delete()
        return Response(status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        #Get the teacher to change
        client = Client.objects.get(person=kwargs['client_id'])

        #Update the person
        person_data = request.data["person"]
        person_ser = PersonSerializer(instance=client.person ,data=person_data)
        if not person_ser.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        person = person_ser.save()

        #Update the client
        client_ser = ModifyClientSerializer(instance = client, data={
                                            "person":person.pk,
                                            "clientstate": request.data["clientstate"],
                                            "balance":request.data["balance"],
                                        })
        if not client_ser.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        client_ser.save()           
        return Response(status=status.HTTP_200_OK)