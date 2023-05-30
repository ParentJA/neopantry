from django.conf import settings
from django.contrib import admin
from django.urls import include, path

import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/accounts/', include(('accounts.urls', 'accounts',))),
    path('api/v1/recipes/', include(('recipes.urls', 'recipes',))),
    path('tinymce/', include('tinymce.urls')),
]

if settings.DEBUG or settings.TESTING_MODE:
    urlpatterns = [
        path('debug/', include(debug_toolbar.urls)),
    ] + urlpatterns
