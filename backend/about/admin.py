from django.contrib import admin
from django.utils.safestring import mark_safe
import nested_admin

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
    LearnMoreContact
)

# ==============================================================================
# ENTERPRISE BASE MIXINS & SINGLETON FRAMEWORKS
# ==============================================================================
class SingletonAdminMixin:
    """
    Mixin ensuring only a single global configuration record can exist 
    for settings or landing-page layout instances.
    """
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

class SingletonModelAdmin(SingletonAdminMixin, admin.ModelAdmin):
    pass

class SingletonNestedModelAdmin(SingletonAdminMixin, nested_admin.NestedModelAdmin):
    pass

class ImagePreviewMixin:
    """
    Reusable administrative utility methods for rendering secure media
    thumbnail reviews inside change lists and detail forms.
    """
    def _render_thumbnail(self, image_field, height=45):
        if image_field:
            try:
                return mark_safe(
                    f'<img src="{image_field.url}" style="max-height: {height}px; width: auto; '
                    f'border: 1px solid #e2e8f0; border-radius: 4px; box-shadow: 0 1px 2px rgba(0,0,0,0.05);" />'
                )
            except Exception:
                pass
        return mark_safe('<span style="color: #a0aec0; font-style: italic;">No Image</span>')

    def _render_detail_preview(self, image_field, height=130):
        if image_field:
            try:
                return mark_safe(
                    f'<div>'
                    f'<a href="{image_field.url}" target="_blank" rel="noopener noreferrer">'
                    f'<img src="{image_field.url}" style="max-height: {height}px; width: auto; '
                    f'border: 1px solid #cbd5e1; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.08); margin-bottom: 6px;" />'
                    f'</a>'
                    f'<p class="help" style="margin: 0; color: #718096;">Click thumbnail to open source file in new tab.</p>'
                    f'</div>'
                )
            except Exception:
                pass
        return mark_safe('<span style="color: #a0aec0; font-style: italic;">No asset uploaded.</span>')

SEO_FIELDSET = ('SEO & Metadata', {
    'classes': ('collapse',),
    'fields': ('meta_title', 'meta_description', 'meta_keywords', 'structured_data'),
    'description': 'Configure search engine parameters and JSON-LD structured tags.'
})

# ==============================================================================
# CMS ADMIN CLASSES
# ==============================================================================
@admin.register(TopBanner)
class TopBannerAdmin(ImagePreviewMixin, SingletonModelAdmin):
    list_display = ('heading', 'badge_text', 'banner_thumbnail', 'created_at')
    readonly_fields = ('created_at', 'image_detail_preview')
    fieldsets = (
        ('Banner Headers', {
            'fields': ('badge_text', 'heading', 'sub_heading')
        }),
        ('Action CTAs', {
            'fields': ('primary_btn_text', 'primary_btn_url', 'secondary_btn_text', 'secondary_btn_url')
        }),
        ('Background Media', {
            'fields': ('image', 'image_detail_preview')
        }),
        SEO_FIELDSET,
    )

    def banner_thumbnail(self, obj):
        return self._render_thumbnail(obj.image, height=45)
    banner_thumbnail.short_description = "Thumbnail"

    def image_detail_preview(self, obj):
        return self._render_detail_preview(obj.image, height=140)
    image_detail_preview.short_description = "Banner Image Preview"


class AboutManifestoDifferentiatorInline(admin.TabularInline):
    model = AboutManifestoDifferentiator
    extra = 2
    fields = ('icon_class', 'title', 'description', 'display_order')


@admin.register(AboutBanner)
class AboutBannerAdmin(ImagePreviewMixin, SingletonModelAdmin):
    list_display = ('heading', 'badge_text', 'charter_badge_subtitle', 'created_at')
    readonly_fields = ('created_at', 'image_detail_preview')
    inlines = [AboutManifestoDifferentiatorInline]
    fieldsets = (
        ('Section Identification', {
            'fields': ('badge_text', 'heading')
        }),
        ('Narrative Copy', {
            'fields': ('content_paragraph_1', 'content_paragraph_2')
        }),
        ('Collage Image & Chartered Badge Overlay', {
            'fields': ('main_image', 'image_detail_preview', 'charter_badge_title', 'charter_badge_subtitle', 'charter_badge_degree')
        }),
    )

    def image_detail_preview(self, obj):
        return self._render_detail_preview(obj.main_image, height=140)
    image_detail_preview.short_description = "Collage Photo Preview"


class AboutVisionItemsInline(nested_admin.NestedTabularInline):
    model = AboutVisionItems
    extra = 2
    fields = ('content', 'created_at')
    readonly_fields = ('created_at',)


class AboutVisionBannerInline(nested_admin.NestedStackedInline):
    model = AboutVisionBanner
    extra = 3
    fk_name = 'about_vision'
    inlines = [AboutVisionItemsInline]
    fields = ('heading', 'content', 'icon_class', 'border_color_class', 'display_order', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(AboutVisionTitle)
class AboutVisionTitleAdmin(SingletonNestedModelAdmin):
    list_display = ('heading', 'badge_text', 'created_at')
    readonly_fields = ('created_at',)
    inlines = [AboutVisionBannerInline]
    fieldsets = (
        (None, {
            'fields': ('badge_text', 'heading', 'sub_heading')
        }),
        SEO_FIELDSET,
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('about_vision_items__items')


class CoreValuesBannerInline(ImagePreviewMixin, admin.StackedInline):
    model = CoreValuesBanner
    extra = 6
    fields = ('heading', 'content', 'icon_class', 'image', 'image_detail_preview', 'display_order', 'created_at')
    readonly_fields = ('created_at', 'image_detail_preview')

    def image_detail_preview(self, obj):
        return self._render_detail_preview(obj.image, height=80)
    image_detail_preview.short_description = "Custom Icon Preview"


@admin.register(CoreValuesTitle)
class CoreValuesTitleAdmin(ImagePreviewMixin, SingletonModelAdmin):
    list_display = ('heading', 'sub_heading', 'created_at')
    readonly_fields = ('created_at',)
    inlines = [CoreValuesBannerInline]
    fieldsets = (
        (None, {
            'fields': ('heading', 'sub_heading')
        }),
        SEO_FIELDSET,
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('core_items')


@admin.register(AboutMetric)
class AboutMetricAdmin(admin.ModelAdmin):
    list_display = ('label', 'target_number', 'prefix', 'suffix', 'sub_label', 'display_order')
    list_editable = ('display_order',)
    ordering = ('display_order',)


class LeadershipBannerInline(ImagePreviewMixin, admin.StackedInline):
    model = LeadershipBanner
    extra = 3
    fields = ('heading', 'designation', 'content', 'image', 'image_detail_preview', 'display_order', 'created_at')
    readonly_fields = ('created_at', 'image_detail_preview')

    def image_detail_preview(self, obj):
        return self._render_detail_preview(obj.image, height=120)
    image_detail_preview.short_description = "Portrait Preview"


@admin.register(LeadershipTitle)
class LeadershipTitleAdmin(SingletonModelAdmin):
    list_display = ('heading', 'badge_text', 'created_at')
    readonly_fields = ('created_at',)
    inlines = [LeadershipBannerInline]
    fieldsets = (
        (None, {
            'fields': ('badge_text', 'heading', 'sub_heading')
        }),
        SEO_FIELDSET,
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('leadership_items')


class CampusOverviewInline(ImagePreviewMixin, admin.StackedInline):
    model = CampusOverview
    extra = 4
    fields = ('title', 'category_badge', 'description', 'icon_class', 'bento_span_class', 'image', 'image_detail_preview', 'display_order', 'created_at')
    readonly_fields = ('created_at', 'image_detail_preview')

    def image_detail_preview(self, obj):
        return self._render_thumbnail(obj.image, height=45)
    image_detail_preview.short_description = "Asset Preview"


@admin.register(CampusTitle)
class CampusTitleAdmin(SingletonModelAdmin):
    list_display = ('heading', 'badge_text', 'created_at')
    readonly_fields = ('created_at',)
    inlines = [CampusOverviewInline]
    fieldsets = (
        (None, {
            'fields': ('badge_text', 'heading', 'sub_heading')
        }),
        SEO_FIELDSET,
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('campus_items')


class VisionResearchBannerInline(admin.TabularInline):
    model = VisionResearchBanner
    extra = 3
    fields = ('heading', 'content', 'display_order', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(VisionResearchTitle)
class VisionResearchTitleAdmin(SingletonModelAdmin):
    list_display = ('heading', 'badge_text', 'created_at')
    readonly_fields = ('created_at',)
    inlines = [VisionResearchBannerInline]
    fieldsets = (
        (None, {
            'fields': ('badge_text', 'heading')
        }),
        SEO_FIELDSET,
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('vision_research_items')


class AchievementBannerInline(admin.TabularInline):
    model = AchievementBanner
    extra = 1
    fields = ('heading', 'content', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(AchievementTitle)
class AchievementTitleAdmin(SingletonModelAdmin):
    list_display = ('heading', 'created_at')
    readonly_fields = ('created_at',)
    inlines = [AchievementBannerInline]
    fieldsets = (
        (None, {
            'fields': ('heading',)
        }),
        SEO_FIELDSET,
    )


@admin.register(LearnMoreContact)
class LearnMoreContactAdmin(SingletonModelAdmin):
    list_display = ('heading', 'mail_id', 'contact', 'created_at')
    readonly_fields = ('created_at',)
    fieldsets = (
        (None, {
            'fields': ('heading', 'sub_heading', 'mail_id', 'contact', 'button_text', 'button_url')
        }),
    )