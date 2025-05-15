from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Core app URLs
    path('', include('myapp.urls')),
    # Users app URLs (to be created)
    # path('users/', include('users.urls')),
    # API URLs
    path('api/', include('api.urls')),
]