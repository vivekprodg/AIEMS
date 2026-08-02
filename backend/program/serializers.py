from rest_framework import serializers
from home.models import Program
from home.serializers import get_absolute_media_url, sanitize_string
from .models import (
    ProgramSummaryPoints,
    AboutProgram,
    AboutProgramFeature,
    ProgramEntryRequirement,
    ProgramEntryRequirementItem,
    CourseDetail,
    CourseDetailChild,
    CourseDetailChildElectiveOption,
    ProgramIndustryCertification,
    CareerOutcomes,
    CareerOutcomeChild,
    ProgramBannerImage,
)


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


class ProgramBannerImageSerializer(BaseCMSSerializer):
    class Meta:
        model = ProgramBannerImage
        fields = ["id", "image"]


class ProgramSummaryPointsSerializer(BaseCMSSerializer):
    class Meta:
        model = ProgramSummaryPoints
        fields = ["id", "icon_image", "icon_class", "title", "value", "sub_text", "display_order"]


class AboutProgramFeatureSerializer(BaseCMSSerializer):
    class Meta:
        model = AboutProgramFeature
        fields = ["id", "title", "description", "icon_class", "display_order"]


class AboutProgramSerializer(BaseCMSSerializer):
    features = AboutProgramFeatureSerializer(many=True, read_only=True)

    class Meta:
        model = AboutProgram
        fields = [
            "id", "small_title", "title", "image", "content",
            "content_paragraph_2", "charter_badge_tag", "charter_badge_title",
            "charter_badge_subtext", "features"
        ]


class ProgramEntryRequirementItemSerializer(BaseCMSSerializer):
    class Meta:
        model = ProgramEntryRequirementItem
        fields = ["id", "content", "display_order"]


class ProgramEntryRequirementSerializer(BaseCMSSerializer):
    items = ProgramEntryRequirementItemSerializer(many=True, read_only=True)

    class Meta:
        model = ProgramEntryRequirement
        fields = ["id", "title", "icon", "icon_class", "content", "items"]


class CourseDetailChildElectiveOptionSerializer(BaseCMSSerializer):
    class Meta:
        model = CourseDetailChildElectiveOption
        fields = [
            "id", "course_name", "course_code", "credit_hours",
            "description", "display_order"
        ]


class CourseDetailChildSerializer(BaseCMSSerializer):
    elective_options = serializers.SerializerMethodField()

    class Meta:
        model = CourseDetailChild
        fields = [
            "id", "course_name", "course_code", "credit_hours",
            "course_type", "is_elective", "description", "elective_options", "display_order"
        ]

    def get_elective_options(self, obj):
        ordered_options = obj.elective_options.all().order_by('display_order', 'id')
        return CourseDetailChildElectiveOptionSerializer(ordered_options, many=True, context=self.context).data


class CourseDetailSerializer(BaseCMSSerializer):
    courses = serializers.SerializerMethodField()

    class Meta:
        model = CourseDetail
        fields = [
            "id", "semester", "title", "credit_summary_text",
            "has_electives", "elective_stream_title", "courses", "display_order"
        ]

    def get_courses(self, obj):
        ordered_courses = obj.courses.all().order_by('display_order', 'id')
        return CourseDetailChildSerializer(ordered_courses, many=True, context=self.context).data


class ProgramIndustryCertificationSerializer(BaseCMSSerializer):
    class Meta:
        model = ProgramIndustryCertification
        fields = [
            "id", "partner_name", "category_badge", "badge_color_class",
            "description", "track_label", "icon_class", "display_order"
        ]


class CareerOutcomeChildSerializer(BaseCMSSerializer):
    class Meta:
        model = CareerOutcomeChild
        fields = ["id", "icon_image", "icon_class", "title", "sub_title", "display_order"]


class CareerOutcomesSerializer(BaseCMSSerializer):
    child_outcomes = serializers.SerializerMethodField()

    class Meta:
        model = CareerOutcomes
        fields = ["id", "title", "content", "child_outcomes"]

    def get_child_outcomes(self, obj):
        ordered_outcomes = obj.child_outcomes.all().order_by('display_order', 'id')
        return CareerOutcomeChildSerializer(ordered_outcomes, many=True, context=self.context).data


class ProgramSerializer(BaseCMSSerializer):
    program_title = serializers.SerializerMethodField()
    program_banner = serializers.SerializerMethodField()
    program_summary = serializers.SerializerMethodField()
    about_programs = serializers.SerializerMethodField()
    entry_requirements = serializers.SerializerMethodField()
    course_details = serializers.SerializerMethodField()
    industry_certifications = serializers.SerializerMethodField()
    career_outcomes = serializers.SerializerMethodField()

    class Meta:
        model = Program
        fields = [
            "id",
            "program_title",
            "icon_image",
            "heading",
            "sub_content",
            "program_banner",
            "program_summary",
            "about_programs",
            "entry_requirements",
            "course_details",
            "industry_certifications",
            "career_outcomes",
        ]

    def get_program_title(self, obj):
        if obj.program_title:
            return sanitize_string(str(obj.program_title.heading if hasattr(obj.program_title, 'heading') else obj.program_title))
        return ""

    def get_program_banner(self, obj):
        last_banner = obj.program_banner.order_by('-created_at').first()
        return ProgramBannerImageSerializer(last_banner, context=self.context).data if last_banner else None

    def get_program_summary(self, obj):
        summaries = obj.program_summary.all().order_by('display_order', 'id')
        return ProgramSummaryPointsSerializer(summaries, many=True, context=self.context).data

    def get_about_programs(self, obj):
        last_obj = obj.about_programs.order_by('-created_at').first()
        if last_obj:
            return AboutProgramSerializer(last_obj, context=self.context).data
        return None

    def get_entry_requirements(self, obj):
        last_obj = obj.entry_requirements.order_by('-created_at').first()
        if last_obj:
            return ProgramEntryRequirementSerializer(last_obj, context=self.context).data
        return None

    def get_course_details(self, obj):
        details = obj.course_details.all().order_by('display_order', 'id')
        return CourseDetailSerializer(details, many=True, context=self.context).data

    def get_industry_certifications(self, obj):
        certs = obj.industry_certifications.all().order_by('display_order', 'id')
        return ProgramIndustryCertificationSerializer(certs, many=True, context=self.context).data

    def get_career_outcomes(self, obj):
        last_obj = obj.career_outcomes.order_by('-created_at').first()
        if last_obj:
            return CareerOutcomesSerializer(last_obj, context=self.context).data
        return None