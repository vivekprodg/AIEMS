import logging
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from .models import (
    TopBanner,
    AboutBanner,
    AboutVisionTitle,
    CoreValuesTitle,
    AboutMetric,
    LeadershipTitle,
    AchievementTitle,
    CampusTitle,
    VisionResearchTitle,
    LearnMoreContact
)
from .serializers import (
    TopBannerSerializer,
    AboutBannerSerializer,
    AboutVisionTitleSerializer,
    CoreValuesTitleSerializer,
    AboutMetricSerializer,
    LeadershipTitleSerializer,
    AchievementTitleSerializer,
    CampusTitleSerializer,
    VisionResearchTitleSerializer,
    LearnMoreContactSerializer
)

logger = logging.getLogger('django')

class ListAboutContentView(APIView):
    """
    Unified API endpoint delivering pre-fetched, high-performance About Us page content.
    Prevents N+1 database queries, enforces deterministic ordering, incorporates cache
    invalidation hooks, and applies DRF rate throttling.
    """
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get(self, request, *args, **kwargs):
        bypass_cache = request.query_params.get('bypass_cache', 'false').lower() == 'true'
        cache_key = 'aiems_about_content_payload'
        cache_timeout = 300  # 5 minutes cache

        if not bypass_cache:
            try:
                cached_data = cache.get(cache_key)
                if cached_data is not None:
                    return Response(cached_data, status=status.HTTP_200_OK)
            except Exception as e:
                logger.warning(
                    f"Cache retrieval failed for '{cache_key}'. Detail: {str(e)}"
                )

        try:
            # Deterministically retrieve the latest singleton records using explicit ordering
            top_banner = TopBanner.objects.order_by('-created_at').first()
            about_banner = AboutBanner.objects.prefetch_related('differentiators').order_by('-created_at').first()
            about_vision_title = AboutVisionTitle.objects.prefetch_related(
                'about_vision_items__items'
            ).order_by('-created_at').first()
            
            core_values_title = CoreValuesTitle.objects.prefetch_related('core_items').order_by('-created_at').first()
            metrics = AboutMetric.objects.all().order_by('display_order', 'id')
            leadership_title = LeadershipTitle.objects.prefetch_related('leadership_items').order_by('-created_at').first()
            achievement_title = AchievementTitle.objects.prefetch_related('achievement_items').order_by('-created_at').first()
            campus_title = CampusTitle.objects.prefetch_related('campus_items').order_by('-created_at').first()
            vision_research_title = VisionResearchTitle.objects.prefetch_related('vision_research_items').order_by('-created_at').first()
            learn_more_contact = LearnMoreContact.objects.order_by('-created_at').first()

            serializer_context = {"request": request}

            response_data = {
                "top_banner": TopBannerSerializer(top_banner, context=serializer_context).data if top_banner else {},
                "about_banner": AboutBannerSerializer(about_banner, context=serializer_context).data if about_banner else {},
                "about_vision": AboutVisionTitleSerializer(about_vision_title, context=serializer_context).data if about_vision_title else {},
                "core_values": CoreValuesTitleSerializer(core_values_title, context=serializer_context).data if core_values_title else {},
                "metrics": AboutMetricSerializer(metrics, many=True, context=serializer_context).data,
                "leadership": LeadershipTitleSerializer(leadership_title, context=serializer_context).data if leadership_title else {},
                "achievements": AchievementTitleSerializer(achievement_title, context=serializer_context).data if achievement_title else {},
                "campus_facilities": CampusTitleSerializer(campus_title, context=serializer_context).data if campus_title else {},
                "vision_research": VisionResearchTitleSerializer(vision_research_title, context=serializer_context).data if vision_research_title else {},
                "learn_more_contact": LearnMoreContactSerializer(learn_more_contact, context=serializer_context).data if learn_more_contact else {}
            }

            if not bypass_cache:
                try:
                    cache.set(cache_key, response_data, timeout=cache_timeout)
                except Exception as e:
                    logger.error(f"Failed to cache About payload under key '{cache_key}'. Detail: {str(e)}")

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Error compiling About Us page content. Detail: {str(e)}", exc_info=True)
            return Response(
                {"error": "An internal system error occurred while generating About Us content."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )