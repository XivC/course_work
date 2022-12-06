
from django.contrib import admin
from django.urls import path, re_path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
   re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('api/', include('planets.urls')),
   path('api/', include('affects.urls')),
   path('admin/', admin.site.urls),
]

