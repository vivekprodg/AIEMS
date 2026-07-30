import logging
from django.core.cache import cache
from rest_framework import viewsets, status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, SAFE_METHODS, AllowAny
from rest_framework.throttling import ScopedRateThrottle

from .models import (
    SiteGlobalSettings,
    NavbarLink,
    AnnouncementTickerItem,
    EligibilityCalculatorConfig,
    ApplyForCourseBanner,
    ApplyForPositionBanner,
    TopBanner,
    HeroTechnicalTag,
    LandingStat,
    AboutBanner,
    Program, 
    IsolatedHomeShowcaseCard,
    CampusFacility,
    NewsEvent,
    AboutBannerTitle,
    ProgramTitle,
    CampusTitle,
    NewsTitle, 
    AdmissionContactDetail,
    AdmissionDetailTitle,
    AdmissionCriteria,
    TeamTitle, 
    TeamFaculty,
    TeamMember,
    ApplyJobDetail,
    ContactUs,
    ApplyCourse,
    ApplyPosition,
    FooterConfig,
    FooterLink,
    FAQCategory,
    FAQItem,
    DynamicPageContent,
    NotificationSetting
)
from .serializers import (
    get_absolute_media_url,
    SiteGlobalSettingsSerializer,
    NavbarLinkSerializer,
    AnnouncementTickerItemSerializer,
    EligibilityCalculatorConfigSerializer,
    TopBannerSerializer,
    HeroTechnicalTagSerializer,
    LandingStatSerializer,
    AboutBannerSerializer,
    ProgramSerializer,
    IsolatedHomeShowcaseCardSerializer,
    CampusFacilitySerializer,
    NewsEventSerializer,
    AboutBannerTitleSerializer, 
    ProgramTitleSerializer,
    CampusTitleSerializer,
    NewsTitleSerializer,
    AdmissionContactDetailSerializer,
    AdmissionDetailTitleSerializer,
    AdmissionCriteriaSerializer,
    TeamTitleSerializer,
    TeamFacultySerializer,
    TeamMemberSerializer,
    ApplyJobDetailSerializer, 
    ContactUsSerializer,
    ApplyCourseSerializer,
    ApplyPositionSerializer,
    ApplyForCourseBannerSerializer,
    ApplyForPositionBannerSerializer,
    FooterConfigSerializer,
    FooterLinkSerializer,
    FAQCategorySerializer,
    FAQItemSerializer,
    DynamicPageContentSerializer
)
from .email_utils import send_submission_emails_async

logger = logging.getLogger('django')

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class AllowCreateOrAdminOnly(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'create':
            return True
        return bool(request.user and request.user.is_staff)


class HomepageCacheInvalidationMixin:
    def perform_create(self, serializer):
        super().perform_create(serializer)
        self.invalidate_cache()

    def perform_update(self, serializer):
        super().perform_update(serializer)
        self.invalidate_cache()

    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        self.invalidate_cache()

    def invalidate_cache(self):
        try:
            cache.delete('aiems_home_content_payload')
            cache.delete('aiems_about_content_payload')
            logger.info("Homepage, Navbar and Footer CMS cache invalidated successfully.")
        except Exception as e:
            logger.error(f"Failed to clear home cache: {str(e)}")


class OptimizedAboutBannerTitleSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = AboutBannerTitle
        fields = '__all__'

    def get_items(self, obj):
        return AboutBannerSerializer(obj.about_banner_items.all(), many=True, context=self.context).data

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get('request')
        if 'image' in ret and instance.image:
            ret['image'] = get_absolute_media_url(request, instance.image)
        return ret


class OptimizedProgramTitleSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    isolated_showcase_cards = serializers.SerializerMethodField()

    class Meta:
        model = ProgramTitle
        fields = ('id', 'heading', 'sub_heading', 'created_at', 'items', 'isolated_showcase_cards')

    def get_items(self, obj):
        return ProgramSerializer(obj.program_items.all(), many=True, context=self.context).data

    def get_isolated_showcase_cards(self, obj):
        active_cards = obj.isolated_showcase_cards.filter(is_active=True).order_by('display_order', '-created_at')
        return IsolatedHomeShowcaseCardSerializer(active_cards, many=True, context=self.context).data


class OptimizedCampusTitleSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = CampusTitle
        fields = ('id', 'heading', 'sub_heading', 'created_at', 'items')

    def get_items(self, obj):
        return CampusFacilitySerializer(obj.campus_items.all(), many=True, context=self.context).data


class OptimizedNewsTitleSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = NewsTitle
        fields = ('id', 'heading', 'sub_heading', 'created_at', 'items')

    def get_items(self, obj):
        return NewsEventSerializer(obj.news_items.all(), many=True, context=self.context).data


class OptimizedAdmissionDetailTitleSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = AdmissionDetailTitle
        fields = ('id', 'heading', 'sub_heading', 'sub_content', 'created_at', 'items')

    def get_items(self, obj):
        return AdmissionCriteriaSerializer(obj.criteria_items.all(), many=True, context=self.context).data


class OptimizedTeamTitleSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = TeamTitle
        fields = ('id', 'heading', 'sub_heading', 'created_at', 'items')

    def get_items(self, obj):
        return TeamFacultySerializer(obj.faculty_items.all(), many=True, context=self.context).data


class FooterLinkCRUDSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterLink
        fields = [
            'id', 'footer_config', 'title', 'url', 
            'display_order', 'is_active', 'open_in_new_tab', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

# ==============================================================================
# CRUD VIEWSETS
# ==============================================================================
class SiteGlobalSettingsViewSet(HomepageCacheInvalidationMixin, viewsets.ModelViewSet):
    queryset = SiteGlobalSettings.objects.all().prefetch_related('navbar_links')
    serializer_class = SiteGlobalSettingsSerializer
    permission_classes = [IsAdminOrReadOnly]


class NavbarLinkViewSet(HomepageCacheInvalidationMixin, viewsets.ModelViewSet):
    queryset = NavbarLink.objects.all().select_related('site_settings')
    serializer_class = NavbarLinkSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        if not (self.request.user and self.request.user.is_staff):
            qs = qs.filter(is_active=True)
        return qs


class AnnouncementTickerItemViewSet(HomepageCacheInvalidationMixin, viewsets.ModelViewSet):
    queryset = AnnouncementTickerItem.objects.all()
    serializer_class = AnnouncementTickerItemSerializer
    permission_classes = [IsAdminOrReadOnly]


class EligibilityCalculatorConfigViewSet(HomepageCacheInvalidationMixin, viewsets.ModelViewSet):
    queryset = EligibilityCalculatorConfig.objects.all()
    serializer_class = EligibilityCalculatorConfigSerializer
    permission_classes = [IsAdminOrReadOnly]


class TopBannerViewSet(HomepageCacheInvalidationMixin, viewsets.ModelViewSet):
    queryset = TopBanner.objects.all().prefetch_related('technical_tags', 'landing_stats')
    serializer_class = TopBannerSerializer
    permission_classes = [IsAdminOrReadOnly]


class AboutBannerViewSet(HomepageCacheInvalidationMixin, viewsets.ModelViewSet):
    queryset = AboutBanner.objects.all()
    serializer_class = AboutBannerSerializer
    permission_classes = [IsAdminOrReadOnly]


class ProgramViewSet(HomepageCacheInvalidationMixin, viewsets.ModelViewSet):
    queryset = Program.objects.all().prefetch_related(
        'program_banner',
        'program_summary',
        'about_programs__features',
        'entry_requirements__items'
    )
    serializer_class = ProgramSerializer
    permission_classes = [IsAdminOrReadOnly]


class IsolatedHomeShowcaseCardViewSet(HomepageCacheInvalidationMixin, viewsets.ModelViewSet):
    queryset = IsolatedHomeShowcaseCard.objects.filter(is_active=True).prefetch_related(
        'isolated_summary_points',
        'isolated_features',
        'isolated_requirements'
    )
    serializer_class = IsolatedHomeShowcaseCardSerializer
    permission_classes = [IsAdminOrReadOnly]


class CampusFacilityViewSet(HomepageCacheInvalidationMixin, viewsets.ModelViewSet):
    queryset = CampusFacility.objects.all()
    serializer_class = CampusFacilitySerializer
    permission_classes = [IsAdminOrReadOnly]


class NewsItemViewSet(HomepageCacheInvalidationMixin, viewsets.ModelViewSet):
    queryset = NewsEvent.objects.all()
    serializer_class = NewsEventSerializer
    permission_classes = [IsAdminOrReadOnly]


class AboutBannerTitleViewSet(HomepageCacheInvalidationMixin, viewsets.ModelViewSet):
    queryset = AboutBannerTitle.objects.all()
    serializer_class = AboutBannerTitleSerializer
    permission_classes = [IsAdminOrReadOnly]


class ProgramTitleViewSet(HomepageCacheInvalidationMixin, viewsets.ModelViewSet):
    queryset = ProgramTitle.objects.all().prefetch_related(
        'program_items__program_banner',
        'program_items__program_summary',
        'program_items__about_programs__features',
        'program_items__entry_requirements__items',
        'isolated_showcase_cards__isolated_summary_points',
        'isolated_showcase_cards__isolated_features',
        'isolated_showcase_cards__isolated_requirements'
    )
    serializer_class = ProgramTitleSerializer
    permission_classes = [IsAdminOrReadOnly]


class CampusTitleViewSet(HomepageCacheInvalidationMixin, viewsets.ModelViewSet):
    queryset = CampusTitle.objects.all()
    serializer_class = CampusTitleSerializer
    permission_classes = [IsAdminOrReadOnly]


class NewsTitleViewSet(HomepageCacheInvalidationMixin, viewsets.ModelViewSet):
    queryset = NewsTitle.objects.all()
    serializer_class = NewsTitleSerializer
    permission_classes = [IsAdminOrReadOnly]


class AdmissionContactDetailViewSet(HomepageCacheInvalidationMixin, viewsets.ModelViewSet):
    queryset = AdmissionContactDetail.objects.all()
    serializer_class = AdmissionContactDetailSerializer
    permission_classes = [IsAdminOrReadOnly]


class AdmissionDetailTitleViewSet(HomepageCacheInvalidationMixin, viewsets.ModelViewSet):
    queryset = AdmissionDetailTitle.objects.all()
    serializer_class = AdmissionDetailTitleSerializer
    permission_classes = [IsAdminOrReadOnly]


class AdmissionCriteriaViewSet(HomepageCacheInvalidationMixin, viewsets.ModelViewSet):
    queryset = AdmissionCriteria.objects.all()
    serializer_class = AdmissionCriteriaSerializer
    permission_classes = [IsAdminOrReadOnly]


class TeamTitleViewSet(HomepageCacheInvalidationMixin, viewsets.ModelViewSet):
    queryset = TeamTitle.objects.all()
    serializer_class = TeamTitleSerializer
    permission_classes = [IsAdminOrReadOnly]


class TeamFacultyViewSet(HomepageCacheInvalidationMixin, viewsets.ModelViewSet):
    queryset = TeamFaculty.objects.all()
    serializer_class = TeamFacultySerializer
    permission_classes = [IsAdminOrReadOnly]


class TeamMemberViewSet(HomepageCacheInvalidationMixin, viewsets.ModelViewSet):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    permission_classes = [IsAdminOrReadOnly]


class ApplyJobDetailViewSet(HomepageCacheInvalidationMixin, viewsets.ModelViewSet):
    queryset = ApplyJobDetail.objects.all()
    serializer_class = ApplyJobDetailSerializer
    permission_classes = [IsAdminOrReadOnly]


class FooterConfigViewSet(HomepageCacheInvalidationMixin, viewsets.ModelViewSet):
    queryset = FooterConfig.objects.all()
    serializer_class = FooterConfigSerializer
    permission_classes = [IsAdminOrReadOnly]


class FooterLinkViewSet(HomepageCacheInvalidationMixin, viewsets.ModelViewSet):
    queryset = FooterLink.objects.all().select_related('footer_config')
    serializer_class = FooterLinkCRUDSerializer
    permission_classes = [IsAdminOrReadOnly]


class FAQCategoryViewSet(HomepageCacheInvalidationMixin, viewsets.ModelViewSet):
    queryset = FAQCategory.objects.all().prefetch_related('faq_items')
    serializer_class = FAQCategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class FAQItemViewSet(HomepageCacheInvalidationMixin, viewsets.ModelViewSet):
    queryset = FAQItem.objects.all().select_related('category')
    serializer_class = FAQItemSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        if not (self.request.user and self.request.user.is_staff):
            qs = qs.filter(is_active=True)
        return qs


class DynamicPageContentViewSet(HomepageCacheInvalidationMixin, viewsets.ModelViewSet):
    queryset = DynamicPageContent.objects.all()
    serializer_class = DynamicPageContentSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'page_key'

    def get_queryset(self):
        qs = super().get_queryset()
        if not (self.request.user and self.request.user.is_staff):
            qs = qs.filter(is_active=True)
        return qs

# ==============================================================================
# UNIFIED HOME LAYOUT API
# ==============================================================================
class ListHomeView(APIView):
    """
    Unified API rendering home layout configuration assets.
    Exposes 100% dynamic CMS content payload including Isolated Homepage Program Showcase details.
    """
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        bypass_cache = request.query_params.get('bypass_cache', 'false').lower() == 'true'
        cache_key = 'aiems_home_content_payload'

        if not bypass_cache:
            cached_data = cache.get(cache_key)
            if cached_data is not None:
                return Response(cached_data, status=status.HTTP_200_OK)

        try:
            site_settings = SiteGlobalSettings.objects.prefetch_related('navbar_links').order_by('-created_at').first()
            tickers = AnnouncementTickerItem.objects.filter(is_active=True).order_by('display_order', '-created_at')
            eligibility_config = EligibilityCalculatorConfig.objects.prefetch_related('stream_options').order_by('-created_at').first()

            top_banner = TopBanner.objects.prefetch_related('technical_tags', 'landing_stats').order_by('-created_at').first()
            about_banner_title = AboutBannerTitle.objects.prefetch_related('about_banner_items').order_by('-created_at').first()
            
            program_title = ProgramTitle.objects.prefetch_related(
                'program_items__program_banner',
                'program_items__program_summary',
                'program_items__about_programs__features',
                'program_items__entry_requirements__items',
                'isolated_showcase_cards__isolated_summary_points',
                'isolated_showcase_cards__isolated_features',
                'isolated_showcase_cards__isolated_requirements'
            ).order_by('-created_at').first()
            
            campus_title = CampusTitle.objects.prefetch_related('campus_items').order_by('-created_at').first()
            news_title = NewsTitle.objects.prefetch_related('news_items').order_by('-created_at').first()
            admission_title = AdmissionDetailTitle.objects.prefetch_related('criteria_items').order_by('-created_at').first()
            admission_contact = AdmissionContactDetail.objects.order_by('-created_at').first()
            team_title = TeamTitle.objects.prefetch_related('faculty_items__member_items').order_by('-created_at').first()
            apply_job = ApplyJobDetail.objects.order_by('-created_at').first()

            footer_config = FooterConfig.objects.prefetch_related('footer_links').order_by('-created_at').first()
            faq_categories = FAQCategory.objects.prefetch_related('faq_items').order_by('display_order', '-created_at')

            serializer_context = {"request": request}

            response_data = {
                "site_settings": SiteGlobalSettingsSerializer(site_settings, context=serializer_context).data if site_settings else {},
                "announcements": AnnouncementTickerItemSerializer(tickers, many=True, context=serializer_context).data,
                "eligibility_config": EligibilityCalculatorConfigSerializer(eligibility_config, context=serializer_context).data if eligibility_config else {},
                "top_banners": TopBannerSerializer(top_banner, context=serializer_context).data if top_banner else {},
                "about_banners": OptimizedAboutBannerTitleSerializer(about_banner_title, context=serializer_context).data if about_banner_title else {},
                "programs": OptimizedProgramTitleSerializer(program_title, context=serializer_context).data if program_title else {},
                "campus_facilities": OptimizedCampusTitleSerializer(campus_title, context=serializer_context).data if campus_title else {},
                "news_events": OptimizedNewsTitleSerializer(news_title, context=serializer_context).data if news_title else {},
                "admission_detail": OptimizedAdmissionDetailTitleSerializer(admission_title, context=serializer_context).data if admission_title else {},
                "admission_contact": AdmissionContactDetailSerializer(admission_contact, context=serializer_context).data if admission_contact else {},
                "teams": OptimizedTeamTitleSerializer(team_title, context=serializer_context).data if team_title else {},
                "apply_job_detail": ApplyJobDetailSerializer(apply_job, context=serializer_context).data if apply_job else {},
                "footer_config": FooterConfigSerializer(footer_config, context=serializer_context).data if footer_config else {},
                "faqs": FAQCategorySerializer(faq_categories, many=True, context=serializer_context).data
            }

            if not bypass_cache:
                cache.set(cache_key, response_data, timeout=300)

            response = Response(response_data, status=status.HTTP_200_OK)
            response["Cache-Control"] = "no-cache, no-store, must-revalidate"
            return response

        except Exception as e:
            logger.error(f"Educational homepage query generation failed. Error context: {str(e)}", exc_info=True)
            return Response(
                {"error": "An internal system error occurred while generating homepage content."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ==============================================================================
# SUBMISSION VIEWSETS WITH NON-BLOCKING DYNAMIC EMAIL TRIGGERS
# ==============================================================================
class ContactUsViewSet(viewsets.ModelViewSet):
    queryset = ContactUs.objects.all().order_by('-created_at')
    serializer_class = ContactUsSerializer
    permission_classes = [AllowCreateOrAdminOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'contact'

    def perform_create(self, serializer):
        instance = serializer.save()
        logger.info(f"New contact inquiry logged. Submission ID: {instance.id}")

        # Trigger dynamic email dispatches asynchronously
        payload = {
            'id': instance.id,
            'name': instance.name,
            'email': instance.email,
            'contact': instance.contact,
            'city': instance.city,
            'message': instance.message,
        }
        send_submission_emails_async('contact', payload)


class ApplyCourseViewSet(viewsets.ModelViewSet):
    queryset = ApplyCourse.objects.all().order_by('-created_at')
    serializer_class = ApplyCourseSerializer
    permission_classes = [AllowCreateOrAdminOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'apply'

    def perform_create(self, serializer):
        instance = serializer.save()
        logger.info(f"Course application logged. Application ID: {instance.id}")

        program_name = instance.program.heading if instance.program else "BSc. CSIT / Academic Program"

        # Trigger dynamic email dispatches asynchronously
        payload = {
            'id': instance.id,
            'name': instance.name,
            'gender': instance.gender,
            'contact': instance.contact,
            'email': instance.email,
            'program_name': program_name,
            'institution': instance.institution,
            'message': instance.message,
        }
        send_submission_emails_async('course', payload)


class ApplyPositionViewSet(viewsets.ModelViewSet):
    queryset = ApplyPosition.objects.all().order_by('-created_at')
    serializer_class = ApplyPositionSerializer
    permission_classes = [AllowCreateOrAdminOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'apply'

    def perform_create(self, serializer):
        instance = serializer.save()
        logger.info(f"Job application submitted. Candidate ID: {instance.id}")

        position_name = instance.position.name if instance.position else "Vacant Position"
        doc_url = get_absolute_media_url(self.request, instance.document) if instance.document else "N/A"

        # Trigger dynamic email dispatches asynchronously
        payload = {
            'id': instance.id,
            'name': instance.name,
            'gender': instance.gender,
            'contact': instance.contact,
            'email': instance.email,
            'position_name': position_name,
            'document_url': doc_url,
            'message': instance.message,
        }
        send_submission_emails_async('job', payload)


class ApplyForCourseBannerViewSet(HomepageCacheInvalidationMixin, viewsets.ModelViewSet):
    queryset = ApplyForCourseBanner.objects.all()
    serializer_class = ApplyForCourseBannerSerializer
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request, *args, **kwargs):
        instance = self.queryset.order_by('-created_at').first()
        if not instance:
            return Response({}, status=status.HTTP_200_OK)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ApplyForPositionBannerViewSet(HomepageCacheInvalidationMixin, viewsets.ModelViewSet):
    queryset = ApplyForPositionBanner.objects.all()
    serializer_class = ApplyForPositionBannerSerializer
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request, *args, **kwargs):
        instance = self.queryset.order_by('-created_at').first()
        if not instance:
            return Response({}, status=status.HTTP_200_OK)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)