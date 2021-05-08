from django.http import Http404
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Bill
from .serializers import BillSerializer

class AllBills(ListCreateAPIView):
    queryset = Bill.objects.select_related()
    serializer_class = BillSerializer
