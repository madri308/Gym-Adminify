from .models import Bill, PayMethod
from rest_framework import serializers
from gymTeachers.models import Teacher,Teachercategory
from gymClients.serializers import ClientSerializer
from gymTeachers.serializers import TeacherSerializer
from gymPersons.serializers import PersonSerializer

class BillSerializer(serializers.ModelSerializer):
    activity = serializers.CharField(source='activity.service',read_only=True)  
    #service = serializers.CharField(source='activity.service',read_only=True) 
    #description = serializers.CharField(source='service.description',read_only=True) 
    clientname = serializers.CharField(source='client.person.name',read_only=True)
    class Meta:
        model = Bill
        fields = (
            "cost",
            "paid",
            "clientname",
            "activity",
            "issuedate",
            "paymethod",
            "paymentday",
            #"description",
            "get_month",
            "get_absolute_url"
        )
        depth = 2
class BillPaymentSerializer(serializers.ModelSerializer):
    activity = serializers.CharField(source='activity.service',read_only=True)  
    #service = serializers.CharField(source='activity.service',read_only=True) 
    #description = serializers.CharField(source='service.description',read_only=True) 
    clientname = serializers.CharField(source='client.person.name',read_only=True)
    class Meta:
        model = Bill
        fields = (
            "cost",
            "paid",
            "clientname",
            "issuedate",
            "activity",
            "paymentday",
            #"description",
            "paymethod",
        )
        depth = 2
class PayMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayMethod
        fields = ("name","id")
