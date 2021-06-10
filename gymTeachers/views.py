from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from django.contrib.auth.models import User

from .models import Teacher,Teachercategory
from .serializers import TeacherSerializer, TeachercategorySerializer, NewTeacherSerializer
from gymPersons.serializers import PersonSerializer,UserofpersonSerializer
from gymPersons.models import Person, Userofperson
from rest_framework import status
from django.db import transaction

class AllTeachers(ListCreateAPIView):
    model = Teacher
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NewTeacherSerializer
        return TeacherSerializer

    def get_queryset(self):
        return Teacher.objects.select_related()
        
    @transaction.atomic
    def create(self, request, pk=None):
        # CREATE THE PERSON
        personSerializer = PersonSerializer(data=request.data["person"])
        personSerializer.is_valid(raise_exception=True)
        personObject = personSerializer.save()

        # CREATE THE USER
        user = User.objects.create_user(request.data["person"]["mail"]
                                        ,request.data["person"]["mail"]
                                        ,request.data["person"]["identification"])
        user.save()
        user.groups.add(4)
        # CREATE RELATION
        userofpersonSerializer = UserofpersonSerializer(data={
                                            'person':personObject.pk,
                                            'user':user.pk })
                                        
        userofpersonSerializer.is_valid(raise_exception=True)
        userofpersonSerializer.save()
        
        # CREATE THE INSTRUCTOR
        serializer = NewTeacherSerializer(data={
                                            'person':personObject.pk,
                                            'teachercategory':request.data["teachercategory"],
                                            "services":request.data["services"],
                                        })
        serializer.is_valid(raise_exception=True)
        saved = serializer.save()
        print(serializer.data)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
            
class AllCategories(ListCreateAPIView):
    queryset = Teachercategory.objects.all()
    serializer_class = TeachercategorySerializer

class AllTeachersByCategory(ListCreateAPIView):
    def get(self, request, category_id, format=None):
        teachers = Teacher.objects.all().filter(teachercategory=category_id)
        serializer = TeacherSerializer(teachers,many=True)
        return Response(serializer.data)

class TeacherDetail(RetrieveUpdateDestroyAPIView):    
    model = Teacher
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return NewTeacherSerializer
        return TeacherSerializer

    def get(self, request, *args, **kwargs):
        teacher = Teacher.objects.get(person=kwargs['teacher_id'])
        serializer = TeacherSerializer(teacher)
        return Response(serializer.data)

    def delete(self, request, teacher_id, format=None):
        # OBTIENE LA RELACION USUARIO PERSONA
        userofpersonRelation = Userofperson.objects.get(person=teacher_id)
        # OBTIENE EL USUARIO Y LO ELIMINA SI EXISTE
        user = User.objects.get(pk = userofpersonRelation.user.pk)
        if user != None:
            user.delete()
        # OBTIENE LA PERSONA Y LA ELIMINA
        person = Person.objects.get(pk=teacher_id)
        person.delete()

        return Response(status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        #Get the teacher to change
        teacher = Teacher.objects.get(person=kwargs['teacher_id'])

        #Update the person
        person_data = request.data.pop('person')
        person_ser = PersonSerializer(instance=teacher.person ,data=person_data)
        if not person_ser.is_valid():
            print(person_ser.errors)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        person_ser.save()

        #Update the teacher
        teacher_ser = NewTeacherSerializer(instance = teacher, data={
                                                                'person':teacher.person.pk,
                                                                'teachercategory':request.data["teachercategory"],
                                                                'services':request.data["services"]
                                                                })
        if not teacher_ser.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        teacher_ser.save()           
                                                     
        return Response(status=status.HTTP_200_OK)
    
