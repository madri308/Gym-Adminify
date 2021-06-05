from .models import Bill, PayMethod
from rest_framework import status
from .serializers import BillPaymentSerializer, BillSerializer, PayMethodSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

class AllBillsOrderedByMonth(ListCreateAPIView):
    queryset = Bill.objects.select_related().order_by('issuedate__month')
    serializer_class = BillSerializer


class BillDetail(RetrieveUpdateDestroyAPIView):
    model = Bill
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return BillPaymentSerializer
        return BillSerializer

    def update(self, request, *args, **kwargs):
        bill = Bill.objects.get(id=kwargs['bill_id'])
        bill_serializer = BillPaymentSerializer(instance=bill, data=request.data)
        if not bill_serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        bill_serializer.save()
        bill.paymethod=PayMethod.objects.get(id=request.data['paymethod'])
        bill.save()
        return Response(status=status.HTTP_200_OK)

class BillPaymentMethods(ListCreateAPIView):
    queryset = PayMethod.objects.all()
    serializer_class = PayMethodSerializer
