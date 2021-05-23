from django.urls import path, include

from AdmSchedule import views

urlpatterns = [
    path('schedules/', views.AllSchedules.as_view()),
    path('schedules/<int:schedule_id>/', views.ScheduleDetails.as_view()),
]
