from django.urls import path, include

from gymServices import views

urlpatterns = [
    path('gym-services/', views.ServiceOne.as_view())
]