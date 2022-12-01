from django.conf import settings
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("home.urls")),
    path('accounts/', include('django.contrib.auth.urls')),
    path("my_app/", include("my_app.urls")),
    path("accommodation/", include("accommodation.urls")),
    path("forum/", include("forum.urls")),
]

if settings.DEBUG:
     from django.conf.urls.static import static
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
