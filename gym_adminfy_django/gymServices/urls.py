from django.urls import path, include

from gymServices import views

urlpatterns = [
    path('services/', views.AllServices.as_view())
]