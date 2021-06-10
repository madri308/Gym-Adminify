from django.urls import path, include

from gymTeachers import views

urlpatterns = [
    path('teachers/', views.AllTeachers.as_view()),
    path('teachersCategories/', views.AllCategories.as_view()),
    path('teachersByCategory/<int:category_id>/', views.AllTeachersByCategory.as_view()),
    path('teachers/<int:teacher_id>/', views.TeacherDetail.as_view()),
    # path('teachers/', views.TeacherDetail.as_view()),
]