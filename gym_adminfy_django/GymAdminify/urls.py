from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('AdmBills.urls')),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('gymPersons.urls')),
    path('api/v1/', include('gymClients.urls')),
    path('api/v1/', include('gymSettings.urls')),
    path('api/v1/', include('gymServices.urls')),
    path('api/v1/', include('gymTeachers.urls')),
    path('api/v1/', include('gymPermissions.urls')),
    path('api/v1/', include('djoser.urls.authtoken')),
]
