# Standard library imports.
from collections import namedtuple

# Django imports.
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

# Third-party imports.
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

__author__ = 'Jason Parent'

Include = namedtuple('Include', ['patterns', 'app_name'])

admin.autodiscover()

schema_view = get_schema_view(
   openapi.Info(
      title="Neopantry API",
      default_version='v1',
      description='Epicurious clone with better features.',
      contact=openapi.Contact(email='jason.a.parent@gmail.com'),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Web app...
    # path('app/', TemplateView.as_view(template_name='index.html')),
    path('api/v1/accounts/', include(Include(patterns='accounts.urls', app_name='accounts'))),
    path('api/v1/recipes/', include(Include(patterns='recipes.urls', app_name='recipes'))),
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='docs'),
    path('', TemplateView.as_view(template_name='index.html')),
    # Static site.
    # path('', TemplateView.as_view(template_name='site.html')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),

# Serves static files in development environment...
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Serves media files in development environment...
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
