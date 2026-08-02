import re
import logging
from rest_framework import serializers
from django.utils.html import escape, strip_tags
from django.conf import settings

from .models import (
    SiteGlobalSettings,
    NavbarLink,
    AnnouncementTickerItem,
    EligibilityCalculatorConfig,
    EligibilityStreamOption,
    HomepagePopupBanner,
    ApplyForCourseBanner,
    ApplyForPositionBanner,
    TopBanner,
    HeroTechnicalTag,
    LandingStat,
    AboutBanner,
    Program,
    IsolatedHomeShowcaseCard,
    IsolatedHomeShowcaseSummaryPoint,
    IsolatedHomeShowcaseFeature,
    IsolatedHomeShowcaseRequirementRule,
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
    Position,
    FooterConfig,
    FooterLink,
    FAQCategory,
    FAQItem,
    DynamicPageContent
)

logger = logging.getLogger('django')

# ==============================================================================
# REUSABLE ENTERPRISE API HELPERS & SANITIZATION UTILITIES
# ==============================================================================
def get_absolute_media_url(request, field_value):
    """
    Safely resolves and builds absolute URIs for media/file assets.
    Ensures 'MEDIA_URL' (/img/) prefix is accurately present on relative assets.
    """
    if not field_value:
        return None
    try:
        url_str = getattr(field_value, 'url', str(field_value))
        if not url_str or url_str == 'False':
            return None

        url_str = str(url_str).strip()

        if url_str.startswith('http://') or url_str.startswith('https://'):
            if 'api.aiems.edu.np' in url_str and url_str.startswith('http://'):
                return url_str.replace('http://', 'https://', 1)
            return url_str

        media_prefix = getattr(settings, 'MEDIA_URL', '/img/').rstrip('/') + '/'
        if not url_str.startswith('/') and not url_str.startswith(media_prefix.lstrip('/')):
            url_str = f"{media_prefix}{url_str.lstrip('/')}"

        if request:
            try:
                absolute_url = request.build_absolute_uri(url_str)
                is_secure = (
                    (hasattr(request, 'is_secure') and request.is_secure()) or 
                    (hasattr(request, 'META') and request.META.get('HTTP_X_FORWARDED_PROTO') == 'https') or
                    'api.aiems.edu.np' in absolute_url
                )
                if is_secure and absolute_url.startswith('http://'):
                    absolute_url = absolute_url.replace('http://', 'https://', 1)
                return absolute_url
            except Exception as e:
                logger.warning(f"Error building absolute URI in get_absolute_media_url: {e}")

        return url_str
    except Exception as e:
        logger.error(f"Error resolving media URL: {e}")
        return None

def sanitize_string(value):
    """
    Mitigates persistent XSS and injection attacks by removing raw HTML tags.
    """
    if not isinstance(value, str):
        return value
    cleaned = strip_tags(value)
    escaped = escape(cleaned)
    return escaped.strip()

def sanitize_serializer_data(attrs):
    for key, value in attrs.items():
        if isinstance(value, str):
            attrs[key] = sanitize_string(value)
    return attrs

def validate_phone_number(value):
    if value:
        cleaned_value = re.sub(r'\s+', '', value)
        if not re.match(r'^\+?1?\d{7,20}$', cleaned_value):
            raise serializers.ValidationError(
                "Phone number must be a valid format (7 to 20 digits, optionally starting with +)."
            )
        return cleaned_value
    return value

def normalize_email_field(email_str):
    if isinstance(email_str, str):
        return email_str.strip().lower()
    return email_str

# ==============================================================================
# GLOBAL & TICKER SERIALIZERS
# ==============================================================================
class NavbarLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = NavbarLink
        fields = [
            'id', 'title', 'url', 'icon_class', 'display_order', 
            'is_active', 'is_button', 'open_in_new_tab', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class SiteGlobalSettingsSerializer(serializers.ModelSerializer):
    navbar_links = serializers.SerializerMethodField()

    class Meta:
        model = SiteGlobalSettings
        fields = '__all__'

    def get_navbar_links(self, obj):
        try:
            if not obj:
                return []
            if hasattr(obj, '_prefetched_objects_cache') and 'navbar_links' in obj._prefetched_objects_cache:
                active_links = [link for link in obj.navbar_links.all() if link.is_active]
                active_links.sort(key=lambda x: (x.display_order, -x.created_at.timestamp() if x.created_at else 0))
            else:
                active_links = obj.navbar_links.filter(is_active=True).order_by('display_order', '-created_at')
            return NavbarLinkSerializer(active_links, many=True, context=self.context).data
        except Exception as e:
            logger.error(f"Error fetching navbar links: {str(e)}")
            return []

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get('request')
        if 'logo' in ret and instance.logo:
            ret['logo'] = get_absolute_media_url(request, instance.logo)
        return ret


class AnnouncementTickerItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnouncementTickerItem
        fields = '__all__'


class EligibilityStreamOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EligibilityStreamOption
        fields = ['id', 'name', 'is_eligible', 'display_order']


class EligibilityCalculatorConfigSerializer(serializers.ModelSerializer):
    stream_options = serializers.SerializerMethodField()

    class Meta:
        model = EligibilityCalculatorConfig
        fields = '__all__'

    def get_stream_options(self, obj):
        if not obj:
            return []
        options = obj.stream_options.all().order_by('display_order', 'id')
        return EligibilityStreamOptionSerializer(options, many=True, context=self.context).data


class HomepagePopupBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomepagePopupBanner
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get('request')

        if 'image' in ret and instance.image:
            ret['image'] = get_absolute_media_url(request, instance.image)

        for key in ['heading', 'sub_heading', 'button_text', 'action_url']:
            if isinstance(ret.get(key), str):
                ret[key] = sanitize_string(ret[key])

        return ret

# ==============================================================================
# STANDARD SYSTEM & HERO TAGS/STATS SERIALIZERS
# ==============================================================================
class HeroTechnicalTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroTechnicalTag
        fields = ['id', 'icon_class', 'title', 'display_order', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class LandingStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandingStat
        fields = ['id', 'target_number', 'prefix', 'suffix', 'label', 'sub_label', 'display_order', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']


class TopBannerSerializer(serializers.ModelSerializer):
    technical_tags = serializers.SerializerMethodField()
    landing_stats = serializers.SerializerMethodField()

    class Meta:
        model = TopBanner
        fields = '__all__'

    def get_technical_tags(self, obj):
        try:
            if not obj:
                return []
            if hasattr(obj, '_prefetched_objects_cache') and 'technical_tags' in obj._prefetched_objects_cache:
                active_tags = [tag for tag in obj.technical_tags.all() if tag.is_active]
                active_tags.sort(key=lambda x: (x.display_order, -x.created_at.timestamp() if x.created_at else 0))
            else:
                active_tags = obj.technical_tags.filter(is_active=True).order_by('display_order', '-created_at')
            return HeroTechnicalTagSerializer(active_tags, many=True, context=self.context).data
        except Exception as e:
            logger.error(f"Error fetching technical tags: {str(e)}")
            return []

    def get_landing_stats(self, obj):
        try:
            if not obj:
                return []
            if hasattr(obj, '_prefetched_objects_cache') and 'landing_stats' in obj._prefetched_objects_cache:
                active_stats = [stat for stat in obj.landing_stats.all() if stat.is_active]
                active_stats.sort(key=lambda x: (x.display_order, -x.created_at.timestamp() if x.created_at else 0))
            else:
                active_stats = obj.landing_stats.filter(is_active=True).order_by('display_order', '-created_at')
            return LandingStatSerializer(active_stats, many=True, context=self.context).data
        except Exception as e:
            logger.error(f"Error fetching landing stats: {str(e)}")
            return []

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get('request')
        if 'image' in ret and instance.image:
            ret['image'] = get_absolute_media_url(request, instance.image)
        return ret


class AboutBannerTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutBannerTitle
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get('request')
        if 'image' in ret and instance.image:
            ret['image'] = get_absolute_media_url(request, instance.image)
        return ret


class AboutBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutBanner
        fields = '__all__'


class ProgramSerializer(serializers.ModelSerializer):
    program_banner = serializers.SerializerMethodField()
    program_summary = serializers.SerializerMethodField()
    about_programs = serializers.SerializerMethodField()
    entry_requirements = serializers.SerializerMethodField()

    class Meta:
        model = Program
        fields = '__all__'

    def get_program_banner(self, obj):
        try:
            banner = obj.program_banner.order_by('-created_at').first()
            if banner and banner.image:
                return {
                    "id": banner.id,
                    "image": get_absolute_media_url(self.context.get('request'), banner.image)
                }
            return None
        except Exception:
            return None

    def get_program_summary(self, obj):
        try:
            request = self.context.get('request')
            items = obj.program_summary.all().order_by('display_order', 'id')
            return [
                {
                    "id": item.id,
                    "title": item.title,
                    "value": item.value,
                    "sub_text": item.sub_text,
                    "icon_class": item.icon_class,
                    "icon_image": get_absolute_media_url(request, item.icon_image) if item.icon_image else None,
                    "display_order": item.display_order,
                }
                for item in items
            ]
        except Exception:
            return []

    def get_about_programs(self, obj):
        try:
            request = self.context.get('request')
            about = obj.about_programs.order_by('-created_at').first()
            if not about:
                return None
            features = about.features.all().order_by('display_order', 'id')
            return {
                "id": about.id,
                "small_title": sanitize_string(about.small_title) if about.small_title else "",
                "title": sanitize_string(about.title) if about.title else "",
                "image": get_absolute_media_url(request, about.image) if about.image else None,
                "content": sanitize_string(about.content) if about.content else "",
                "content_paragraph_2": sanitize_string(about.content_paragraph_2) if about.content_paragraph_2 else "",
                "charter_badge_tag": sanitize_string(about.charter_badge_tag) if about.charter_badge_tag else "",
                "charter_badge_title": sanitize_string(about.charter_badge_title) if about.charter_badge_title else "",
                "charter_badge_subtext": sanitize_string(about.charter_badge_subtext) if about.charter_badge_subtext else "",
                "features": [
                    {
                        "id": f.id,
                        "title": sanitize_string(f.title) if f.title else "",
                        "description": sanitize_string(f.description) if f.description else "",
                        "icon_class": f.icon_class or "",
                        "display_order": f.display_order
                    }
                    for f in features
                ]
            }
        except Exception:
            return None

    def get_entry_requirements(self, obj):
        try:
            request = self.context.get('request')
            entry = obj.entry_requirements.order_by('-created_at').first()
            if not entry:
                return None
            items = entry.items.all().order_by('display_order', 'id')
            return {
                "id": entry.id,
                "title": sanitize_string(entry.title) if entry.title else "",
                "icon": get_absolute_media_url(request, entry.icon) if entry.icon else None,
                "icon_class": entry.icon_class or "",
                "content": sanitize_string(entry.content) if entry.content else "",
                "items": [
                    {
                        "id": item.id,
                        "content": sanitize_string(item.content) if item.content else "",
                        "display_order": item.display_order
                    }
                    for item in items
                ]
            }
        except Exception:
            return None

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get('request')
        if 'icon_image' in ret and instance.icon_image:
            ret['icon_image'] = get_absolute_media_url(request, instance.icon_image)
        return ret

# ==============================================================================
# ISOLATED HOMEPAGE SHOWCASE SERIALIZERS
# ==============================================================================
class IsolatedHomeShowcaseSummaryPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = IsolatedHomeShowcaseSummaryPoint
        fields = ['id', 'title', 'value', 'sub_text', 'icon_class', 'display_order']


class IsolatedHomeShowcaseFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = IsolatedHomeShowcaseFeature
        fields = ['id', 'title', 'description', 'icon_class', 'display_order']


class IsolatedHomeShowcaseRequirementRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = IsolatedHomeShowcaseRequirementRule
        fields = ['id', 'content', 'display_order']


class IsolatedHomeShowcaseCardSerializer(serializers.ModelSerializer):
    summary_points = serializers.SerializerMethodField()
    features = serializers.SerializerMethodField()
    requirements = serializers.SerializerMethodField()
    banner_image = serializers.SerializerMethodField()
    target_program_id = serializers.ReadOnlyField(source='target_program.id')

    class Meta:
        model = IsolatedHomeShowcaseCard
        fields = [
            'id', 'heading', 'sub_content', 'banner_image', 'status_badge_text', 
            'cohort_tag', 'charter_badge_tag', 'specializations_title', 
            'prerequisite_title', 'prerequisite_overview', 'apply_button_text', 
            'eligibility_button_text', 'syllabus_button_text', 
            'custom_syllabus_redirect_url', 'target_program_id',
            'display_order', 'is_active', 'summary_points', 'features', 'requirements'
        ]

    def get_banner_image(self, obj):
        request = self.context.get('request')
        if obj.banner_image:
            return get_absolute_media_url(request, obj.banner_image)
        return None

    def get_summary_points(self, obj):
        points = obj.isolated_summary_points.all().order_by('display_order', 'id')
        return IsolatedHomeShowcaseSummaryPointSerializer(points, many=True, context=self.context).data

    def get_features(self, obj):
        feats = obj.isolated_features.all().order_by('display_order', 'id')
        return IsolatedHomeShowcaseFeatureSerializer(feats, many=True, context=self.context).data

    def get_requirements(self, obj):
        rules = obj.isolated_requirements.all().order_by('display_order', 'id')
        return IsolatedHomeShowcaseRequirementRuleSerializer(rules, many=True, context=self.context).data

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        for key in ['heading', 'sub_content', 'charter_badge_tag', 'specializations_title', 'prerequisite_title', 'prerequisite_overview']:
            if isinstance(ret.get(key), str):
                ret[key] = sanitize_string(ret[key])
        return ret


class CampusFacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CampusFacility
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get('request')
        if 'image' in ret and instance.image:
            ret['image'] = get_absolute_media_url(request, instance.image)
        return ret


class NewsEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsEvent
        fields = '__all__'


class ProgramTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramTitle
        fields = '__all__'


class CampusTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampusTitle
        fields = '__all__'


class NewsTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsTitle
        fields = '__all__'


class AdmissionContactDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdmissionContactDetail
        fields = '__all__'


class AdmissionDetailTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdmissionDetailTitle
        fields = '__all__'


class AdmissionCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdmissionCriteria
        fields = '__all__'


class TeamTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamTitle
        fields = '__all__'


class TeamFacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamFaculty
        fields = '__all__'


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get('request')
        if 'profile_image' in ret and instance.profile_image:
            ret['profile_image'] = get_absolute_media_url(request, instance.profile_image)
        return ret


class ApplyJobDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplyJobDetail
        fields = '__all__'

# ==============================================================================
# SECURE FORM SUBMISSION SERIALIZERS
# ==============================================================================
class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = ['id', 'name', 'email', 'contact', 'city', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_contact(self, value):
        return validate_phone_number(value)

    def validate(self, attrs):
        required_fields = ['name', 'email', 'city']
        for field in required_fields:
            if not attrs.get(field):
                raise serializers.ValidationError({"error": f"{field} is required"})

        attrs = sanitize_serializer_data(attrs)

        if 'email' in attrs:
            attrs['email'] = normalize_email_field(attrs['email'])

        return attrs


class ApplyCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplyCourse
        fields = [
            'id', 'name', 'gender', 'contact', 'email',
            'program', 'institution', 'message', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def validate_contact(self, value):
        return validate_phone_number(value)

    def validate(self, attrs):
        required_fields = ['name', 'gender', 'contact', 'email', 'institution']
        for field in required_fields:
            if not attrs.get(field):
                raise serializers.ValidationError({"error": f"{field} is required"})

        attrs = sanitize_serializer_data(attrs)

        if 'email' in attrs:
            attrs['email'] = normalize_email_field(attrs['email'])

        return attrs


class ApplyPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplyPosition
        fields = [
            'id', 'name', 'gender', 'contact', 'email',
            'position', 'document', 'message', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def validate_contact(self, value):
        return validate_phone_number(value)

    def validate(self, attrs):
        required_fields = [
            'name', 'gender', 'contact', 'email',
            'position', 'document', 'message'
        ]
        for field in required_fields:
            if not attrs.get(field):
                raise serializers.ValidationError({"error": f"{field} is required"})

        attrs = sanitize_serializer_data(attrs)

        if 'email' in attrs:
            attrs['email'] = normalize_email_field(attrs['email'])

        return attrs

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get('request')
        if 'document' in ret and instance.document:
            ret['document'] = get_absolute_media_url(request, instance.document)
        return ret

# ==============================================================================
# LANDING BANNER SERIALIZERS
# ==============================================================================
class ApplyForCourseBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplyForCourseBanner
        fields = ["id", "heading", "sub_heading", "image"]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get('request')
        if 'image' in ret and instance.image:
            ret['image'] = get_absolute_media_url(request, instance.image)
        return ret


class ApplyForPositionBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplyForPositionBanner
        fields = ["id", "heading", "sub_heading", "image"]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get('request')
        if 'image' in ret and instance.image:
            ret['image'] = get_absolute_media_url(request, instance.image)
        return ret

# ==============================================================================
# GLOBAL FOOTER CONFIGURATION SERIALIZERS
# ==============================================================================
class FooterLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterLink
        fields = [
            'id', 'category', 'title', 'url', 'display_order', 
            'is_active', 'open_in_new_tab', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class FooterConfigSerializer(serializers.ModelSerializer):
    footer_links = serializers.SerializerMethodField()

    class Meta:
        model = FooterConfig
        fields = [
            'id', 'logo', 'branding_description', 'facebook_url', 
            'linkedin_url', 'instagram_url', 'footer_links', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def get_footer_links(self, obj):
        try:
            if not obj:
                return []
            if hasattr(obj, '_prefetched_objects_cache') and 'footer_links' in obj._prefetched_objects_cache:
                active_links = [link for link in obj.footer_links.all() if link.is_active]
                active_links.sort(key=lambda x: (x.category, x.display_order, -x.created_at.timestamp() if x.created_at else 0))
            else:
                active_links = obj.footer_links.filter(is_active=True).order_by('category', 'display_order', '-created_at')
            return FooterLinkSerializer(active_links, many=True, context=self.context).data
        except Exception as e:
            logger.error(f"Error fetching footer links: {str(e)}")
            return []

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get('request')
        if instance and hasattr(instance, 'logo') and instance.logo:
            ret['logo'] = get_absolute_media_url(request, instance.logo)
        else:
            ret['logo'] = None
        return ret

# ==============================================================================
# CMS FAQ & DYNAMIC PAGE CONTENT SERIALIZERS
# ==============================================================================
class FAQItemSerializer(serializers.ModelSerializer):
    category_slug = serializers.ReadOnlyField(source='category.slug')

    class Meta:
        model = FAQItem
        fields = [
            'id', 'category', 'category_slug', 'question', 
            'answer', 'is_active', 'display_order', 'created_at'
        ]
        read_only_fields = ['id', 'category_slug', 'created_at']


class FAQCategorySerializer(serializers.ModelSerializer):
    faq_items = serializers.SerializerMethodField()

    class Meta:
        model = FAQCategory
        fields = ['id', 'name', 'slug', 'display_order', 'faq_items', 'created_at']
        read_only_fields = ['id', 'slug', 'created_at']

    def get_faq_items(self, obj):
        try:
            if hasattr(obj, '_prefetched_objects_cache') and 'faq_items' in obj._prefetched_objects_cache:
                active_items = [item for item in obj.faq_items.all() if item.is_active]
                active_items.sort(key=lambda x: (x.display_order, -x.created_at.timestamp() if x.created_at else 0))
            else:
                active_items = obj.faq_items.filter(is_active=True).order_by('display_order', '-created_at')
            return FAQItemSerializer(active_items, many=True, context=self.context).data
        except Exception:
            return []


class DynamicPageContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DynamicPageContent
        fields = [
            'id', 'page_key', 'title', 'subtitle', 'content_json',
            'is_active', 'meta_title', 'meta_description', 'meta_keywords',
            'structured_data', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']