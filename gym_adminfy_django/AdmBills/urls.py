from django.urls import path, include

from AdmBills import views

urlpatterns = [
    path('bills/', views.AllBills.as_view()),
]