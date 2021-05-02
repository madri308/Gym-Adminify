from django.http import Http404

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Person
from .serializers import PersonSerializer


class AllPersons(APIView):
    def get(self, request, format=None):
        person = Person.objects.objects.all()
        serializer = PersonSerializer(teachers,many=True)
        return Response(serializer.data)
