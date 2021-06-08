from django.urls import path, include

from gymActivities import views

urlpatterns = [
    path('activities/', views.ActivitiesWithSettings.as_view()),
    path('activities/<int:activity_id>/', views.ActivityDetail.as_view()),
    path('activities-enroll/<int:activity_id>/', views.ActivityEnrollClients.as_view()),
    path('update-activities/', views.ActivityDetail.as_view()),
    path('schedule-activities/', views.AllScheduleActivities.as_view()),
]