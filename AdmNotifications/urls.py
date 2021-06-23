from django.urls import path, include

from AdmNotifications import views

urlpatterns = [
    path('notifications/', views.AllNotifications.as_view()),
]