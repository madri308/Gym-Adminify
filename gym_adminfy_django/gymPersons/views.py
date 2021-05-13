from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Person
from .serializers import PersonSerializer
from rest_framework import status


class AllPersons(APIView):
    def get(self, request, format=None):
        person = Person.objects.all()
        serializer = PersonSerializer(person,many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = PersonSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
