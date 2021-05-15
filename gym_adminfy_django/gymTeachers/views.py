from django.http import Http404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Teacher,Teachercategory
from gymPersons.models import Person
from .serializers import TeacherSerializer, TeachercategorySerializer, NewTeacherSerializer
from gymPersons.serializers import PersonSerializer


class AllTeachers(ListCreateAPIView):
    model = Teacher
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NewTeacherSerializer
        return TeacherSerializer

    def get_queryset(self):
        return Teacher.objects.select_related()
        
    def create(self, request, pk=None):
        ##CREA LA PERSONA
        person = PersonSerializer(data=request.data["person"])
        if not person.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        personObject = person.save()

        ##CREA EL INSTRUCTOR
        serializer = NewTeacherSerializer(data={
                                            'person':personObject.pk,
                                            'teachercategory':request.data["teachercategory"],
                                            "services":request.data["services"],
                                        })
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        
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
        teacher = Teacher.objects.get(person=teacher_id)
        teacher.delete()
        return Response(status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        #Get the teacher to change
        teacher = Teacher.objects.get(person=kwargs['teacher_id'])

        #Update the person
        person_data = request.data.pop('person')
        person_ser = PersonSerializer(instance=teacher.person ,data=person_data)
        if not person_ser.is_valid():
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
    
