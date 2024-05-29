# school_management/urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('core.urls')),
    path('api/', include('schools.urls')),  # Assurez-vous que cette application est correctement configurée
    path('api/', include('academics.urls')),  # Assurez-vous que cette application est correctement configurée
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
