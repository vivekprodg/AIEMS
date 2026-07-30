from rest_framework import serializers
from home.serializers import get_absolute_media_url, sanitize_string
from .models import (
    TopBanner,
    AboutBanner,
    AboutManifestoDifferentiator,
    AboutVisionTitle,
    AboutVisionBanner,
    AboutVisionItems,
    CoreValuesTitle,
    CoreValuesBanner,
    AboutMetric,
    LeadershipTitle,
    LeadershipBanner,
    AchievementTitle,
    AchievementBanner,
    CampusTitle,
    CampusOverview,
    VisionResearchTitle,
    VisionResearchBanner,
    LearnMoreContact,
)

# ==============================================================================
# ENTERPRISE BASE SERIALIZER FOR MEDIA RESOLUTION & XSS SANITIZATION
# ==============================================================================
class BaseCMSSerializer(serializers.ModelSerializer):
    """
    Base Serializer that handles:
    1. Unified resolution of absolute media URLs for ImageField and FileField.
    2. Deep output-level XSS protection by sanitizing all serialized string fields.
    """
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get('request')

        # Dynamically resolve absolute media URLs
        for field_name, field in self.fields.items():
            if isinstance(field, (serializers.ImageField, serializers.FileField)):
                file_value = getattr(instance, field_name, None)
                if file_value:
                    ret[field_name] = get_absolute_media_url(request, file_value)

        # Enforce output sanitization against persistent XSS
        for key, value in ret.items():
            if isinstance(value, str):
                ret[key] = sanitize_string(value)

        return ret

# ==============================================================================
# CMS SERIALIZERS
# ==============================================================================
class TopBannerSerializer(BaseCMSSerializer):
    class Meta:
        model = TopBanner
        fields = '__all__'


class AboutManifestoDifferentiatorSerializer(BaseCMSSerializer):
    class Meta:
        model = AboutManifestoDifferentiator
        fields = '__all__'


class AboutBannerSerializer(BaseCMSSerializer):
    differentiators = AboutManifestoDifferentiatorSerializer(many=True, read_only=True)

    class Meta:
        model = AboutBanner
        fields = '__all__'


class AboutVisionItemsSerializer(BaseCMSSerializer):
    class Meta:
        model = AboutVisionItems
        fields = '__all__'


class AboutVisionBannerSerializer(BaseCMSSerializer):
    items = AboutVisionItemsSerializer(many=True, read_only=True)

    class Meta:
        model = AboutVisionBanner
        fields = '__all__'


class AboutVisionTitleSerializer(BaseCMSSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = AboutVisionTitle
        fields = '__all__'

    def get_items(self, obj):
        return AboutVisionBannerSerializer(
            obj.about_vision_items.all().order_by('display_order', '-created_at'), 
            many=True, 
            context=self.context
        ).data


class CoreValuesBannerSerializer(BaseCMSSerializer):
    class Meta:
        model = CoreValuesBanner
        fields = '__all__'


class CoreValuesTitleSerializer(BaseCMSSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = CoreValuesTitle
        fields = '__all__'

    def get_items(self, obj):
        return CoreValuesBannerSerializer(
            obj.core_items.all().order_by('display_order', '-created_at'), 
            many=True, 
            context=self.context
        ).data


class AboutMetricSerializer(BaseCMSSerializer):
    class Meta:
        model = AboutMetric
        fields = '__all__'


class LeadershipBannerSerializer(BaseCMSSerializer):
    class Meta:
        model = LeadershipBanner
        fields = '__all__'


class LeadershipTitleSerializer(BaseCMSSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = LeadershipTitle
        fields = '__all__'

    def get_items(self, obj):
        return LeadershipBannerSerializer(
            obj.leadership_items.all().order_by('display_order', '-created_at'), 
            many=True, 
            context=self.context
        ).data


class AchievementBannerSerializer(BaseCMSSerializer):
    class Meta:
        model = AchievementBanner
        fields = '__all__'


class AchievementTitleSerializer(BaseCMSSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = AchievementTitle
        fields = '__all__'

    def get_items(self, obj):
        return AchievementBannerSerializer(
            obj.achievement_items.all(), 
            many=True, 
            context=self.context
        ).data


class CampusOverviewSerializer(BaseCMSSerializer):
    class Meta:
        model = CampusOverview
        fields = '__all__'


class CampusTitleSerializer(BaseCMSSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = CampusTitle
        fields = '__all__'

    def get_items(self, obj):
        return CampusOverviewSerializer(
            obj.campus_items.all().order_by('display_order', '-created_at'), 
            many=True, 
            context=self.context
        ).data


class VisionResearchBannerSerializer(BaseCMSSerializer):
    class Meta:
        model = VisionResearchBanner
        fields = '__all__'


class VisionResearchTitleSerializer(BaseCMSSerializer):
    items = serializers.SerializerMethodField()

    class Meta:
        model = VisionResearchTitle
        fields = '__all__'

    def get_items(self, obj):
        return VisionResearchBannerSerializer(
            obj.vision_research_items.all().order_by('display_order', '-created_at'), 
            many=True, 
            context=self.context
        ).data


class LearnMoreContactSerializer(BaseCMSSerializer):
    class Meta:
        model = LearnMoreContact
        fields = '__all__'

# Backwards compatibility alias
LearMoreContactSerializer = LearnMoreContactSerializer