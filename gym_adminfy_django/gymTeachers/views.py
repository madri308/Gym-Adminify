from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Teacher
from .serializers import TeacherSerializer


class AllTeachers(APIView):
    def get(self, request, format=None):
        teachers = Teacher.objects.select_related('TeacherCategory')
        serializer = TeacherSerializer(teachers,many=True)
        return Response(serializer.data)