from django.urls import path, include

from gymClients import views

urlpatterns = [
    path('clients/', views.AllClients.as_view()),
    path('clients/<int:client_id>/', views.ClientDetail.as_view()),
   # path('teachers/', views.TeacherDetail.as_view()),
]