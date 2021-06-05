from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Person
from .serializers import PersonSerializer, UserofpersonSerializer
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from django.views.decorators.http import require_http_methods

class AllPersons(ListCreateAPIView):
    model = Person
    def get_serializer_class(self):
        return PersonSerializer
    def get_queryset(self):
        return Person.objects.all()

    def post(request):
        #CREATE THE PERSON
        personSerializer = PersonSerializer(data=request.data["person"])
        personSerializer.is_valid(raise_exception=True)
        personObject = personSerializer.save()
        # CREATE THE USER
        user = User.objects.create_user(request.data["person"]["mail"], request.data["person"]["mail"], request.data["person"]["identification"])
        user.save()
        # #CREATE RELATION
        userofpersonSerializer = UserofpersonSerializer(data={
                                            'person':personObject.pk,
                                            'user':user.pk
                                        })
        userofpersonSerializer.is_valid(raise_exception=True)
        userofpersonSerializer.save()
        return Response(personSerializer.data["id"],status=status.HTTP_201_CREATED)