from django.urls import path, include

from AdmBills import views

urlpatterns = [
    path('billsByMonth/', views.AllBillsOrderedByMonth.as_view()),
    path('billsByMonth/<int:bill_id>/', views.BillDetail.as_view()),
    path('billsPaymentMethods/', views.BillPaymentMethods.as_view()),
]