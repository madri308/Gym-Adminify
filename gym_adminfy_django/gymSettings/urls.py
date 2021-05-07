from django.urls import path, include
from django.contrib.auth.decorators import permission_required

from gymSettings import views

urlpatterns = [
    path('gym-config/', views.OneConfig.as_view()),
    path('gym-info/', permission_required('view_config')(views.OneGym.as_view())),
    path('room-info/', views.OneRoom.as_view()),
]