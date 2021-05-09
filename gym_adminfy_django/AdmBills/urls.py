from django.urls import path, include

from AdmBills import views

urlpatterns = [
    path('billsByMonth/', views.AllBillsOrderedByMonth.as_view()),
    path('billsByClient/', views.AllBillsOrderedByClient.as_view()),
    #path('billsByActivity/', views.AllBillsOrderedByActivity.as_view()),
]