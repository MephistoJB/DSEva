from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/repositories/', include('repository.urls')),
    path('api/content/', include('dseva_content.urls')),
]
