from django.urls import path, include

from gymPermissions import views

urlpatterns = [
    path('permissions/', views.AllPermissionsGroup.as_view()),
]