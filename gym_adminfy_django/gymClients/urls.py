from django.urls import path, include

from gymClients import views

urlpatterns = [
    path('clients/', views.AllClients.as_view()),
]