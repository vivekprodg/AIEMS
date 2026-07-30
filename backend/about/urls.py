from django.urls import path
from .views import ListAboutContentView

# Namespace configuration for reverse URL resolution
app_name = 'about'

urlpatterns = [
    # Unified API endpoint delivering compiled, pre-fetched About Us page content
    path(
        'about-content/',
        ListAboutContentView.as_view(),
        name='about-content'
    ),
]