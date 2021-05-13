from django.http import Http404
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Teacher,Teachercategory
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
                                            'teachercategory':request.data["teacher"]["teachercategory"]
                                        })
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        
        return Response(status=status.HTTP_201_CREATED)
            
class AllCategories(ListCreateAPIView):
    queryset = Teachercategory.objects.all()
    serializer_class = TeachercategorySerializer

class AllTeachersByCategory(APIView):
    def get(self, request, category_id, format=None):
        teachers = Teacher.objects.all().filter(teachercategory=category_id)
        serializer = TeacherSerializer(teachers,many=True)
        return Response(serializer.data)

# class TeacherNames(APIView):
#     def get(self,request,format = None):
#         teacherNames = Teacher.objects.all().only('person')
#         serializer = TeacherNamesSerializer(teacherNames,many=True)
#         return Response(serializer.data)

# class TeacherDetail(APIView):
#     def get_object(self, product_id):
#         try:
#             return Teacher.objects.get(person=product_id)
#         except Product.DoesNotExist:
#             raise Http404
    
#     def get(self, request, product_id, format=None):
#         teacher = self.get_object(product_id)
#         serializer = TeacherSerializer(teacher)
#         return Response(serializer.data)
