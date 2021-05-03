from django.urls import path, include

from gymTeachers import views

urlpatterns = [
    path('teachers/', views.AllTeachers.as_view()),
    path('teachersNames/', views.TeacherNames.as_view()),
]