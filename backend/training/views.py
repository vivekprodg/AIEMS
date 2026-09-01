import logging
from django.core.cache import cache
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.throttling import ScopedRateThrottle, AnonRateThrottle, UserRateThrottle

from home.views import AllowCreateOrAdminOnly
from home.email_utils import send_submission_emails_async
from .models import TrainingPageBanner, TrainingApplicationLead
from .serializers import TrainingPageBannerSerializer, TrainingApplicationLeadSerializer

logger = logging.getLogger('django')

# ==============================================================================
# 1. UNIFIED DYNAMIC PAGE CONTENT VIEW (WITH CACHING & PREFETCH)
# ==============================================================================
class TrainingPageContentView(APIView):
    """
    Delivers compiled, pre-fetched Training page content in a single query.
    Prevents N+1 database queries, enforces deterministic ordering,
    and supports cache bypass parameters.
    """
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get(self, request, *args, **kwargs):
        bypass_cache = request.query_params.get('bypass_cache', 'false').lower() == 'true'
        cache_key = 'aiems_training_content_payload'
        cache_timeout = 300  # 5 minutes cache

        if not bypass_cache:
            try:
                cached_data = cache.get(cache_key)
                if cached_data is not None:
                    return Response(cached_data, status=status.HTTP_200_OK)
            except Exception as e:
                logger.warning(f"Cache retrieval failed for '{cache_key}': {str(e)}")

        try:
            banner = TrainingPageBanner.objects.prefetch_related(
                'modules',
                'time_slots',
                'perks',
                'stream_options',
                'timeframe_options',
                'delivery_modes',
                'experience_levels'
            ).order_by('-created_at').first()

            serializer_context = {"request": request}
            response_data = TrainingPageBannerSerializer(banner, context=serializer_context).data if banner else {}

            if not bypass_cache:
                try:
                    cache.set(cache_key, response_data, timeout=cache_timeout)
                except Exception as e:
                    logger.error(f"Failed to set cache key '{cache_key}': {str(e)}")

            response = Response(response_data, status=status.HTTP_200_OK)
            response["Cache-Control"] = "no-cache, no-store, must-revalidate"
            return response

        except Exception as e:
            logger.error(f"Error compiling Training Page CMS content: {str(e)}", exc_info=True)
            return Response(
                {"error": "An internal system error occurred while generating training content."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# ==============================================================================
# 2. PUBLIC APPLICATION LEAD CAPTURE VIEWSET
# ==============================================================================
class TrainingApplicationViewSet(viewsets.ModelViewSet):
    """
    Handles student registration submissions with scoped throttling (anti-spam)
    and non-blocking background email notifications.
    """
    queryset = TrainingApplicationLead.objects.all().order_by('-created_at')
    serializer_class = TrainingApplicationLeadSerializer
    permission_classes = [AllowCreateOrAdminOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'apply'

    def perform_create(self, serializer):
        instance = serializer.save()
        logger.info(f"New Training Registration Lead logged: #{instance.id} ({instance.ref_id})")

        # Prepare payload for non-blocking asynchronous email dispatch
        payload = {
            'id': instance.id,
            'ref_id': instance.ref_id,
            'name': instance.full_name,
            'gender': instance.gender,
            'contact': instance.phone,
            'whatsapp': instance.whatsapp or instance.phone,
            'email': instance.email,
            'academic_stream': instance.academic_stream,
            'institution': instance.institution,
            'selected_modules': instance.selected_modules,
            'timeframe': instance.timeframe,
            'time_slot': instance.time_slot,
            'training_mode': instance.training_mode,
            'experience_level': instance.experience_level,
            'learning_goal': instance.learning_goal,
        }

        try:
            send_submission_emails_async('training', payload)
        except Exception as ex:
            logger.warning(f"Asynchronous email dispatcher for training lead #{instance.id} triggered note: {ex}")