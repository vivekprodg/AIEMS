from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrainingPageContentView, TrainingApplicationViewSet

app_name = 'training'

router = DefaultRouter()
router.register(r'apply', TrainingApplicationViewSet, basename='training-apply')

urlpatterns = [
    # Static page & modules endpoint
    path('content/', TrainingPageContentView.as_view(), name='training-content'),
    # Form submission endpoints
    path('', include(router.urls)),
]