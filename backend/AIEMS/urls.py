"""
URL configuration for AIEMS project.
Guarantees robust routing for CMS endpoints and media serving.
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from django.views.static import serve

urlpatterns = [
    # Admin Control Panel
    path('aiems-control-admin-panel/', admin.site.urls),

    # Core System & CMS API Routes
    path('api/home/', include('home.urls')),
    path('api/about/', include('about.urls')),
    path('api/program/', include('program.urls')),
    path('api/training/', include('training.urls')),

    # Direct media route guaranteeing asset delivery under /img/ in development & production
    re_path(r'^img/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)