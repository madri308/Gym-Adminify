from django.http import Http404
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Teacher,Teachercategory
from .serializers import TeacherSerializer,TeacherNamesSerializer, TeachercategorySerializer

class AllTeachers(ListCreateAPIView):
    queryset = Teacher.objects.select_related()
    serializer_class = TeacherSerializer

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
