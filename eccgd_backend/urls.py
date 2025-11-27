from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Base URL patterns required for all environments
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

# --- DEVELOPMENT/DEBUG ONLY URLS ---
if settings.DEBUG:
    # 1. Imports for Swagger/OpenAPI schema are now inside the DEBUG block
    from rest_framework import permissions
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi

    schema_view = get_schema_view(
        openapi.Info(
            title="LMS Backend API",
            default_version='v1',
            description="API documentation for LMS Backend",
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )

    # 2. Append Swagger/Redoc paths only in DEBUG mode
    urlpatterns += [
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ]

    # 3. Append static/media file serving (already here, but good practice)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)