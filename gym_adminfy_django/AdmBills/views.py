from django.http import Http404
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Bill
from .serializers import BillSerializer

# class AllBillsOrderedByActivity(ListCreateAPIView):
#     queryset = Bill.objects.select_related().order_by('activity')
#     serializer_class = BillSerializer

class AllBillsOrderedByClient(ListCreateAPIView):
    queryset = Bill.objects.select_related().order_by('client')
    serializer_class = BillSerializer

class AllBillsOrderedByMonth(ListCreateAPIView):
    queryset = Bill.objects.select_related().order_by('issuedate__month')
    serializer_class = BillSerializer