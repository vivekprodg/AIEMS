"""
URL configuration for AIEMS project.
Guarantees robust media serving for uploaded CMS assets.
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path
from django.views.static import serve

urlpatterns = [
    path('aiems-control-admin-panel/', admin.site.urls),
    path('api/home/', include('home.urls')),
    path('api/about/', include('about.urls')),
    path('api/program/', include('program.urls')),

    # Direct media route guaranteeing asset delivery under /img/ in development
    re_path(r'^img/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)