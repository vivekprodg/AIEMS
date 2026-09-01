from rest_framework import serializers
from home.serializers import (
    get_absolute_media_url,
    sanitize_string,
    sanitize_serializer_data,
    validate_phone_number,
    normalize_email_field
)
from .models import (
    TrainingPageBanner,
    TrainingCurriculumModule,
    TrainingTimeSlot,
    TrainingSidebarPerk,
    TrainingStreamOption,
    TrainingTimeframeOption,
    TrainingDeliveryMode,
    TrainingExperienceLevel,
    TrainingApplicationLead
)

# ==============================================================================
# BASE CMS SERIALIZER WITH XSS ENCRYPTION & URL ESCAPING
# ==============================================================================
class BaseCMSSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get('request')

        for field_name, field in self.fields.items():
            if isinstance(field, (serializers.ImageField, serializers.FileField)):
                file_value = getattr(instance, field_name, None)
                if file_value:
                    ret[field_name] = get_absolute_media_url(request, file_value)

        for key, value in ret.items():
            if isinstance(value, str):
                ret[key] = sanitize_string(value)

        return ret

# ==============================================================================
# NESTED CONFIGURATION SERIALIZERS
# ==============================================================================
class TrainingCurriculumModuleSerializer(BaseCMSSerializer):
    class Meta:
        model = TrainingCurriculumModule
        fields = ['id', 'title', 'description', 'icon_class', 'display_order', 'is_active']

class TrainingTimeSlotSerializer(BaseCMSSerializer):
    class Meta:
        model = TrainingTimeSlot
        fields = ['id', 'time_range', 'slot_tag', 'display_order', 'is_active']

class TrainingSidebarPerkSerializer(BaseCMSSerializer):
    class Meta:
        model = TrainingSidebarPerk
        fields = ['id', 'title', 'icon_class', 'display_order']

class TrainingStreamOptionSerializer(BaseCMSSerializer):
    class Meta:
        model = TrainingStreamOption
        fields = ['id', 'name', 'display_order', 'is_active']

class TrainingTimeframeOptionSerializer(BaseCMSSerializer):
    class Meta:
        model = TrainingTimeframeOption
        fields = ['id', 'name', 'display_order', 'is_active']

class TrainingDeliveryModeSerializer(BaseCMSSerializer):
    class Meta:
        model = TrainingDeliveryMode
        fields = ['id', 'name', 'display_order', 'is_active']

class TrainingExperienceLevelSerializer(BaseCMSSerializer):
    class Meta:
        model = TrainingExperienceLevel
        fields = ['id', 'name', 'display_order', 'is_active']

class TrainingPageBannerSerializer(BaseCMSSerializer):
    modules = serializers.SerializerMethodField()
    time_slots = serializers.SerializerMethodField()
    perks = serializers.SerializerMethodField()
    stream_options = serializers.SerializerMethodField()
    timeframe_options = serializers.SerializerMethodField()
    delivery_modes = serializers.SerializerMethodField()
    experience_levels = serializers.SerializerMethodField()

    class Meta:
        model = TrainingPageBanner
        fields = '__all__'

    def get_modules(self, obj):
        active_modules = obj.modules.filter(is_active=True).order_by('display_order', 'id')
        return TrainingCurriculumModuleSerializer(active_modules, many=True, context=self.context).data

    def get_time_slots(self, obj):
        active_slots = obj.time_slots.filter(is_active=True).order_by('display_order', 'id')
        return TrainingTimeSlotSerializer(active_slots, many=True, context=self.context).data

    def get_perks(self, obj):
        ordered_perks = obj.perks.all().order_by('display_order', 'id')
        return TrainingSidebarPerkSerializer(ordered_perks, many=True, context=self.context).data

    def get_stream_options(self, obj):
        active_streams = obj.stream_options.filter(is_active=True).order_by('display_order', 'id')
        return TrainingStreamOptionSerializer(active_streams, many=True, context=self.context).data

    def get_timeframe_options(self, obj):
        active_timeframes = obj.timeframe_options.filter(is_active=True).order_by('display_order', 'id')
        return TrainingTimeframeOptionSerializer(active_timeframes, many=True, context=self.context).data

    def get_delivery_modes(self, obj):
        active_modes = obj.delivery_modes.filter(is_active=True).order_by('display_order', 'id')
        return TrainingDeliveryModeSerializer(active_modes, many=True, context=self.context).data

    def get_experience_levels(self, obj):
        active_levels = obj.experience_levels.filter(is_active=True).order_by('display_order', 'id')
        return TrainingExperienceLevelSerializer(active_levels, many=True, context=self.context).data

# ==============================================================================
# SECURE LEAD SUBMISSION SERIALIZER
# ==============================================================================
class TrainingApplicationLeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingApplicationLead
        fields = [
            'id', 'ref_id', 'full_name', 'gender', 'phone',
            'whatsapp', 'email', 'academic_stream', 'institution',
            'selected_modules', 'timeframe', 'time_slot', 'training_mode',
            'experience_level', 'learning_goal', 'created_at'
        ]
        read_only_fields = ['id', 'ref_id', 'created_at']

    def validate_phone(self, value):
        return validate_phone_number(value)

    def validate(self, attrs):
        required_fields = ['full_name', 'gender', 'phone', 'email', 'academic_stream', 'institution']
        for field in required_fields:
            if not attrs.get(field):
                raise serializers.ValidationError({field: f"Field '{field}' is mandatory."})

        # Sanitize text payloads against persistent XSS
        attrs = sanitize_serializer_data(attrs)

        if 'email' in attrs:
            attrs['email'] = normalize_email_field(attrs['email'])

        return attrs