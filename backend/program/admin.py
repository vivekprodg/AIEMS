from django.contrib import admin
from django.utils.safestring import mark_safe
from django.core.cache import cache
import nested_admin

from home.models import Program
from .models import (
    ProgramBannerImage,
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
)


def clear_program_cms_caches():
    try:
        cache.clear()
    except Exception:
        pass


class ImagePreviewMixin:
    def _render_thumbnail(self, image_field, height=40):
        if image_field:
            try:
                if hasattr(image_field, 'url') and image_field.url:
                    return mark_safe(
                        f'<img src="{image_field.url}" style="max-height: {height}px; width: auto; '
                        f'border: 1px solid #cbd5e1; border-radius: 4px; box-shadow: 0 1px 2px rgba(0,0,0,0.05);" />'
                    )
            except Exception:
                pass
        return mark_safe('<span style="color: #a0aec0; font-style: italic;">No Asset</span>')

    def _render_detail_preview(self, image_field, height=120):
        if image_field:
            try:
                if hasattr(image_field, 'url') and image_field.url:
                    return mark_safe(
                        f'<div>'
                        f'<a href="{image_field.url}" target="_blank" rel="noopener noreferrer">'
                        f'<img src="{image_field.url}" style="max-height: {height}px; width: auto; '
                        f'border: 1px solid #cbd5e1; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.08); margin-bottom: 4px;" />'
                        f'</a>'
                        f'<p class="help" style="margin: 0; color: #718096; font-size: 11px;">Click thumbnail to inspect full asset.</p>'
                        f'</div>'
                    )
            except Exception:
                pass
        return mark_safe('<span style="color: #a0aec0; font-style: italic;">No asset uploaded.</span>')


class ProgramBannerImageInline(ImagePreviewMixin, nested_admin.NestedTabularInline):
    model = ProgramBannerImage
    extra = 1
    fields = ('image', 'banner_preview', 'created_at')
    readonly_fields = ('banner_preview', 'created_at')

    def banner_preview(self, obj):
        return self._render_thumbnail(obj.image, height=45)
    banner_preview.short_description = "Banner Preview"


class ProgramSummaryPointsInline(ImagePreviewMixin, nested_admin.NestedTabularInline):
    model = ProgramSummaryPoints
    extra = 6
    fields = ('title', 'value', 'sub_text', 'icon_class', 'icon_image', 'icon_preview', 'display_order')
    readonly_fields = ('icon_preview',)

    def icon_preview(self, obj):
        return self._render_thumbnail(obj.icon_image, height=35)
    icon_preview.short_description = "Custom Icon"


class AboutProgramFeatureInline(nested_admin.NestedTabularInline):
    model = AboutProgramFeature
    extra = 2
    fields = ('title', 'description', 'icon_class', 'display_order')


class AboutProgramInline(ImagePreviewMixin, nested_admin.NestedStackedInline):
    model = AboutProgram
    extra = 1
    inlines = [AboutProgramFeatureInline]
    fieldsets = (
        ('Header & Narrative Copy', {
            'fields': ('small_title', 'title', 'content', 'content_paragraph_2')
        }),
        ('Overview Image & Affiliation Badge Overlay', {
            'fields': (
                'image', 'image_preview',
                'charter_badge_tag', 'charter_badge_title', 'charter_badge_subtext'
            )
        }),
    )
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        return self._render_detail_preview(obj.image, height=110)
    image_preview.short_description = "Overview Image Preview"


class ProgramEntryRequirementItemInline(nested_admin.NestedTabularInline):
    model = ProgramEntryRequirementItem
    extra = 4
    fields = ('content', 'display_order')


class ProgramEntryRequirementInline(ImagePreviewMixin, nested_admin.NestedStackedInline):
    model = ProgramEntryRequirement
    extra = 1
    inlines = [ProgramEntryRequirementItemInline]
    fields = ('title', 'icon', 'icon_preview', 'icon_class', 'content')
    readonly_fields = ('icon_preview',)

    def icon_preview(self, obj):
        return self._render_thumbnail(obj.icon, height=40)
    icon_preview.short_description = "Icon Preview"


class CourseDetailChildElectiveOptionInline(nested_admin.NestedTabularInline):
    model = CourseDetailChildElectiveOption
    extra = 3
    fields = ('course_code', 'course_name', 'credit_hours', 'description', 'display_order')


class CourseDetailChildInline(nested_admin.NestedStackedInline):
    model = CourseDetailChild
    extra = 4
    inlines = [CourseDetailChildElectiveOptionInline]
    fields = (
        'course_name', 'course_code', 'credit_hours',
        'course_type', 'is_elective', 'description', 'display_order'
    )


class ProgramIndustryCertificationInline(nested_admin.NestedStackedInline):
    model = ProgramIndustryCertification
    extra = 4
    fields = (
        'partner_name', 'category_badge', 'badge_color_class',
        'track_label', 'icon_class', 'description', 'display_order'
    )


class CareerOutcomeChildInline(ImagePreviewMixin, nested_admin.NestedTabularInline):
    model = CareerOutcomeChild
    extra = 6
    fields = ('title', 'sub_title', 'icon_class', 'icon_image', 'icon_preview', 'display_order')
    readonly_fields = ('icon_preview',)

    def icon_preview(self, obj):
        return self._render_thumbnail(obj.icon_image, height=35)
    icon_preview.short_description = "Icon"


class CareerOutcomesInline(nested_admin.NestedStackedInline):
    model = CareerOutcomes
    extra = 1
    inlines = [CareerOutcomeChildInline]
    fields = ('title', 'content')


@admin.register(Program)
class ProgramAdmin(nested_admin.NestedModelAdmin):
    inlines = [
        ProgramBannerImageInline,
        ProgramSummaryPointsInline,
        AboutProgramInline,
        ProgramEntryRequirementInline,
        ProgramIndustryCertificationInline,
        CareerOutcomesInline,
    ]
    list_display = ("heading", "program_title", "created_at")
    search_fields = ("heading", "sub_content")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        clear_program_cms_caches()

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        clear_program_cms_caches()


@admin.register(CourseDetail)
class CourseDetailAdmin(nested_admin.NestedModelAdmin):
    inlines = [CourseDetailChildInline]
    list_display = ("program", "semester", "title", "has_electives", "display_order")
    list_editable = ("display_order",)
    list_filter = ("program", "has_electives")
    search_fields = ("title", "semester")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        clear_program_cms_caches()

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        clear_program_cms_caches()


@admin.register(CareerOutcomes)
class CareerOutcomesAdmin(nested_admin.NestedModelAdmin):
    inlines = [CareerOutcomeChildInline]
    list_display = ("title", "program", "created_at")
    list_filter = ("program",)
    search_fields = ("title", "content")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        clear_program_cms_caches()

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        clear_program_cms_caches()