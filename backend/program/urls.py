from django.urls import path
from .views import ProgramDetailView

# Namespace configuration for reverse URL resolution across Django apps
app_name = 'program'

urlpatterns = [
    # Detail API endpoint for fetching dynamic academic program specifications
    path(
        "<int:id>/",
        ProgramDetailView.as_view(),
        name="program-detail"
    ),
]