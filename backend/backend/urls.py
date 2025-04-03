from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('back.urls')),
    path('api/', include('back.urls')),
    path('admin/', admin.site.urls),
    # path('api/', include('heritage.urls')),
    # path('api/', include('heritage.urls')),  # Assuming you have this path for the API
    path('accounts/', include('allauth.urls')),  # Google login endpoint


]
# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)