import logging
from django.core.cache import cache
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from home.models import Program
from .serializers import ProgramSerializer

logger = logging.getLogger('django')


class ProgramDetailView(RetrieveAPIView):
    """
    Unified API endpoint for individual academic program specifications.
    Employs relational prefetching to eliminate N+1 queries, includes backend
    caching with bypass parameters, applies rate throttling, and logs exceptions.
    """
    queryset = Program.objects.all().prefetch_related(
        'program_banner',
        'program_summary',
        'about_programs__features',
        'entry_requirements__items',
        'course_details__courses',
        'industry_certifications',
        'career_outcomes__child_outcomes'
    )
    serializer_class = ProgramSerializer
    lookup_field = "id"
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def retrieve(self, request, *args, **kwargs):
        program_id = kwargs.get(self.lookup_field)
        bypass_cache = request.query_params.get('bypass_cache', 'false').lower() == 'true'
        cache_key = f'aiems_program_detail_payload_{program_id}'
        cache_timeout = 300  # 5 minutes cache

        # 1. Attempt Cache Retrieval
        if not bypass_cache:
            try:
                cached_data = cache.get(cache_key)
                if cached_data is not None:
                    return Response(cached_data, status=status.HTTP_200_OK)
            except Exception as e:
                logger.warning(
                    f"Program detail cache retrieval failed for '{cache_key}'. Detail: {str(e)}"
                )

        # 2. Database Retrieval & Serialization
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            response_data = serializer.data

            # 3. Store Payload in Cache
            if not bypass_cache:
                try:
                    cache.set(cache_key, response_data, timeout=cache_timeout)
                except Exception as e:
                    logger.error(
                        f"Failed to set cache key '{cache_key}' for Program ID {program_id}. Detail: {str(e)}"
                    )

            return Response(response_data, status=status.HTTP_200_OK)

        except Program.DoesNotExist:
            return Response(
                {"error": f"Academic program with ID '{program_id}' was not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(
                f"Error processing Program detail endpoint for ID {program_id}. Detail: {str(e)}",
                exc_info=True
            )
            return Response(
                {"error": "An internal system error occurred while retrieving program specifications."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )