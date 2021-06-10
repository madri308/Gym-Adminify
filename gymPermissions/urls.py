from django.urls import path, include

from gymPermissions import views

urlpatterns = [
    path('permissions/', views.GetPermissionsByUser.as_view()),
]