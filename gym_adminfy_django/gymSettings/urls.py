from django.urls import path, include

from gymSettings import views

urlpatterns = [
    path('gym-config/', views.ConfigOne.as_view())
]