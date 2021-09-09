from django.urls import path, include
from gymPersons import views

urlpatterns = [
    path('persons/', views.AllPersons.as_view()),
    path('personInfo/', views.PersonDetail.as_view()),
]