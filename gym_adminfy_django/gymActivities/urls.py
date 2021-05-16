from django.urls import path, include

from gymActivities import views

urlpatterns = [
    path('activities/', views.AllActivities.as_view()),
    path('schedule-activities/', views.AllScheduleActivities.as_view()),
    #path('activities/', views.AllActivities.as_view()),
    #path('clientsPerActivity/<int:activity_id>', views.AllClientsByActivity.as_view()),
]
