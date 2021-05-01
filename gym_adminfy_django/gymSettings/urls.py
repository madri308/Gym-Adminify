from django.urls import path, include

from gymSettings import views

urlpatterns = [
    path('gym-config/', views.OneConfig.as_view()),
    path('gym-info/', views.OneGym.as_view()),
    path('room-info/', views.OneRoom.as_view()),
]