from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Person, Userofperson
from .serializers import PersonSerializer, UserofpersonSerializer,CurrentUserSerializer
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework import status, authentication, permissions
from gymClients.models import Client
from gymTeachers.models import Teacher
from gymClients.serializers import ClientSerializer
from gymTeachers.serializers import JustDataTeacherSerializer
from django.core import serializers


class PersonDetail(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        data = {}
        if Userofperson.objects.filter(user=request.user).exists():
            # OBTENEMOS LA RELACION USUARIO PERSONA
            userofpersonRelation = Userofperson.objects.get(user=request.user)
            if Client.objects.filter(person = userofpersonRelation.person).exists():
                clientObject = Client.objects.get(person = userofpersonRelation.person.pk)
                data = ClientSerializer(clientObject).data
            elif Teacher.objects.filter(person = userofpersonRelation.person).exists():
                teacherObject = Teacher.objects.get(person = userofpersonRelation.person.pk)
                data = JustDataTeacherSerializer(teacherObject).data
        else:
            data = CurrentUserSerializer(User.objects.get(pk = request.user.id)).data
        # print(data)
        return Response(data)

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

