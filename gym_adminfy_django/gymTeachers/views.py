from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Teacher
from .serializers import TeacherSerializer,TeacherNamesSerializer


class AllTeachers(APIView):
    def get(self, request, format=None):
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers,many=True)
        return Response(serializer.data)

class TeacherNames(APIView):
    def get(self,request,format = None):
        teacherNames = Teacher.objects.all().only('person')
        serializer = TeacherNamesSerializer(teacherNames,many=True)
        return Response(serializer.data)
