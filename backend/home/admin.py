from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.core.cache import cache
import nested_admin

from .models import (
    SiteGlobalSettings, NavbarLink, AnnouncementTickerItem, EligibilityCalculatorConfig,
    EligibilityStreamOption, TopBanner, HeroTechnicalTag, LandingStat, AboutBannerTitle, AboutBanner,
    ProgramTitle, Program,
    IsolatedHomeShowcaseCard, IsolatedHomeShowcaseSummaryPoint, IsolatedHomeShowcaseFeature, IsolatedHomeShowcaseRequirementRule,
    CampusTitle, CampusFacility, NewsTitle, NewsEvent, AdmissionContactDetail,
    AdmissionDetailTitle, AdmissionCriteria, TeamTitle, TeamFaculty, TeamMember,
    ApplyJobDetail, ContactUs, ApplyCourse, Position, ApplyPosition,
    ApplyForCourseBanner, ApplyForPositionBanner, FooterConfig, FooterLink,
    FAQCategory, FAQItem, DynamicPageContent, NotificationSetting
)

# ==============================================================================
# CUSTOM DJANGO ADMIN SITE HEADER & TITLES
# ==============================================================================
admin.site.site_header = "AIEMS Admin Panel"
admin.site.site_title = "AIEMS College Management"
admin.site.index_title = "AIEMS CMS & Admissions Control"

def clear_all_cms_caches():
    """
    Clears all active CMS layout response payloads across all cache providers.
    """
    try:
        cache.delete('aiems_home_content_payload')
        cache.delete('aiems_about_content_payload')
    except Exception:
        pass

# ==============================================================================
# ENTERPRISE DJANGO ADMIN HELPERS & UTILITY MIXINS
# ==============================================================================
class SingletonAdminMixin:
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        clear_all_cms_caches()

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        clear_all_cms_caches()


class EducationAdminMixin:
    def _render_thumbnail(self, image_field, height=40):
        if image_field:
            try:
                if hasattr(image_field, 'url') and image_field.url:
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
                if hasattr(image_field, 'url') and image_field.url:
                    return mark_safe(
                        f'<div>'
                        f'<a href="{image_field.url}" target="_blank">'
                        f'<img src="{image_field.url}" style="max-height: {height}px; width: auto; '
                        f'border: 1px solid #cbd5e1; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.08); margin-bottom: 6px;" />'
                        f'</a>'
                        f'<p class="help" style="margin: 0; color: #718096;">Click on image thumbnail to open source file in a new tab.</p>'
                        f'</div>'
                    )
            except Exception:
                pass
        return mark_safe('<span style="color: #a0aec0; font-style: italic;">No current asset uploaded.</span>')

SEO_FIELDSET = ('SEO & Metadata', {
    'classes': ('collapse',),
    'fields': ('meta_title', 'meta_description', 'meta_keywords', 'structured_data'),
    'description': 'Configure search engine parameters and structured Schema.org JSON-LD tags.'
})

# ==============================================================================
# 1. GLOBAL SITE SETTINGS, HEADER NAVBAR LINKS & ANNOUNCEMENT TICKERS
# ==============================================================================
class NavbarLinkInline(admin.TabularInline):
    model = NavbarLink
    extra = 1
    fields = ('title', 'url', 'icon_class', 'display_order', 'is_active', 'is_button', 'open_in_new_tab', 'created_at')
    readonly_fields = ('created_at',)
    ordering = ('display_order', '-created_at')


@admin.register(SiteGlobalSettings)
class SiteGlobalSettingsAdmin(EducationAdminMixin, SingletonAdminMixin, admin.ModelAdmin):
    list_display = ('site_title', 'primary_phone', 'primary_email', 'location_address', 'created_at')
    readonly_fields = ('created_at', 'logo_detail_preview')
    inlines = [NavbarLinkInline]
    fieldsets = (
        ('Site Identity & Hotlines', {
            'fields': ('site_title', 'primary_phone', 'primary_email', 'location_address')
        }),
        ('Branding Assets & Maps', {
            'fields': ('logo', 'logo_detail_preview', 'map_iframe_url')
        }),
        SEO_FIELDSET,
    )

    def logo_detail_preview(self, obj):
        return self._render_detail_preview(obj.logo, height=100)
    logo_detail_preview.short_description = "Logo Preview"

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('navbar_links')


@admin.register(NavbarLink)
class NavbarLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'display_order', 'is_active', 'is_button', 'open_in_new_tab', 'created_at')
    list_filter = ('is_active', 'is_button', 'open_in_new_tab', 'created_at')
    search_fields = ('title', 'url', 'icon_class')
    list_editable = ('display_order', 'is_active', 'is_button', 'open_in_new_tab')
    readonly_fields = ('created_at',)
    ordering = ('display_order', '-created_at')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        clear_all_cms_caches()


@admin.register(AnnouncementTickerItem)
class AnnouncementTickerItemAdmin(admin.ModelAdmin):
    list_display = ('badge_label', 'text_content', 'target_url', 'is_active', 'display_order', 'created_at')
    list_editable = ('is_active', 'display_order')
    search_fields = ('badge_label', 'text_content')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        clear_all_cms_caches()


class EligibilityStreamOptionInline(admin.TabularInline):
    model = EligibilityStreamOption
    extra = 3
    fields = ('name', 'is_eligible', 'display_order')
    ordering = ('display_order', 'id')


@admin.register(EligibilityCalculatorConfig)
class EligibilityCalculatorConfigAdmin(SingletonAdminMixin, admin.ModelAdmin):
    list_display = ('heading', 'min_cgpa', 'min_percentage', 'created_at')
    inlines = [EligibilityStreamOptionInline]
    fieldsets = (
        ('Header & Instructions', {
            'fields': ('heading', 'sub_heading', 'required_stream_text')
        }),
        ('Minimum Grade Thresholds', {
            'fields': ('min_cgpa', 'min_percentage')
        }),
        ('Response Messages', {
            'fields': ('eligible_message', 'ineligible_message')
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('stream_options')

# ==============================================================================
# 2. CORE LANDING BANNER & CMS PRESENTATION ADMINS
# ==============================================================================
class HeroTechnicalTagInline(admin.TabularInline):
    model = HeroTechnicalTag
    extra = 4
    fields = ('icon_class', 'title', 'display_order', 'is_active', 'created_at')
    readonly_fields = ('created_at',)
    ordering = ('display_order', '-created_at')


class LandingStatInline(admin.TabularInline):
    model = LandingStat
    extra = 4
    fields = ('target_number', 'prefix', 'suffix', 'label', 'sub_label', 'display_order', 'is_active', 'created_at')
    readonly_fields = ('created_at',)
    ordering = ('display_order', '-created_at')


@admin.register(TopBanner)
class TopBannerAdmin(EducationAdminMixin, SingletonAdminMixin, admin.ModelAdmin):
    list_display = ('heading', 'trimmed_sub_heading', 'banner_thumbnail', 'created_at')
    readonly_fields = ('created_at', 'image_detail_preview')
    inlines = [HeroTechnicalTagInline, LandingStatInline]
    fieldsets = (
        ('Main Content', {
            'fields': ('heading', 'sub_heading')
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
    image_detail_preview.short_description = "Image Preview"

    def trimmed_sub_heading(self, obj):
        if obj.sub_heading and len(obj.sub_heading) > 75:
            return f"{obj.sub_heading[:72]}..."
        return obj.sub_heading or "-"
    trimmed_sub_heading.short_description = "Sub Heading"

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('technical_tags', 'landing_stats')


class AboutBannerInline(admin.TabularInline):
    model = AboutBanner
    extra = 2
    fields = ('icon_class', 'heading', 'content', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(AboutBannerTitle)
class AboutBannerTitleAdmin(EducationAdminMixin, SingletonAdminMixin, admin.ModelAdmin):
    list_display = ('heading', 'badge_text', 'banner_image_thumbnail', 'created_at')
    readonly_fields = ('created_at', 'image_detail_preview')
    inlines = [AboutBannerInline]
    fieldsets = (
        ('Section Identification & Badges', {
            'fields': ('badge_text', 'heading')
        }),
        ('Narrative Paragraphs', {
            'fields': ('sub_heading', 'content_paragraph_2')
        }),
        ('Featured Image & Glass Card Overlay Badge', {
            'fields': (
                'image', 'image_detail_preview',
                'floating_badge_icon_class', 'floating_badge_title', 'floating_badge_subtitle'
            )
        }),
        ('Action CTAs & Links', {
            'fields': (
                'primary_btn_text', 'primary_btn_url',
                'secondary_btn_text', 'secondary_btn_url'
            )
        }),
        SEO_FIELDSET,
    )

    def banner_image_thumbnail(self, obj):
        return self._render_thumbnail(obj.image, height=45)
    banner_image_thumbnail.short_description = "Image Thumbnail"

    def image_detail_preview(self, obj):
        return self._render_detail_preview(obj.image, height=140)
    image_detail_preview.short_description = "Image Preview"

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('about_banner_items')


@admin.register(AboutBanner)
class AboutBannerAdmin(admin.ModelAdmin):
    list_display = ('heading', 'about_title', 'icon_class', 'trimmed_content', 'created_at')
    list_filter = ('about_title', 'created_at')
    search_fields = ('heading', 'content', 'icon_class')
    list_select_related = ('about_title',)
    readonly_fields = ('created_at',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        clear_all_cms_caches()

    def trimmed_content(self, obj):
        if obj.content and len(obj.content) > 75:
            return f"{obj.content[:72]}..."
        return obj.content or "-"
    trimmed_content.short_description = "Content"

# ==============================================================================
# 3. ACADEMIC PROGRAM LAYOUT & ISOLATED HOMEPAGE SHOWCASE ADMINS
# ==============================================================================
class ProgramInline(EducationAdminMixin, admin.StackedInline):
    model = Program
    extra = 1
    fields = ('heading', 'icon_image', 'icon_preview_thumbnail', 'sub_content', 'created_at')
    readonly_fields = ('created_at', 'icon_preview_thumbnail')

    def icon_preview_thumbnail(self, obj):
        return self._render_thumbnail(obj.icon_image, height=35)
    icon_preview_thumbnail.short_description = "Current Icon"


class IsolatedHomeShowcaseSummaryPointInline(admin.TabularInline):
    model = IsolatedHomeShowcaseSummaryPoint
    extra = 3
    fields = ('title', 'value', 'sub_text', 'icon_class', 'display_order')


class IsolatedHomeShowcaseFeatureInline(admin.TabularInline):
    model = IsolatedHomeShowcaseFeature
    extra = 6
    fields = ('title', 'description', 'icon_class', 'display_order')


class IsolatedHomeShowcaseRequirementRuleInline(admin.TabularInline):
    model = IsolatedHomeShowcaseRequirementRule
    extra = 3
    fields = ('content', 'display_order')


@admin.register(IsolatedHomeShowcaseCard)
class IsolatedHomeShowcaseCardAdmin(EducationAdminMixin, admin.ModelAdmin):
    list_display = ('heading', 'status_badge_text', 'target_program', 'display_order', 'is_active', 'banner_thumbnail', 'created_at')
    list_editable = ('display_order', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('heading', 'sub_content', 'charter_badge_tag', 'specializations_title')
    readonly_fields = ('created_at', 'image_detail_preview')
    inlines = [
        IsolatedHomeShowcaseSummaryPointInline,
        IsolatedHomeShowcaseFeatureInline,
        IsolatedHomeShowcaseRequirementRuleInline
    ]
    fieldsets = (
        ('Showcase Card Headings & Degree Target', {
            'fields': ('program_title', 'target_program', 'heading', 'status_badge_text', 'cohort_tag', 'charter_badge_tag')
        }),
        ('Specializations & Narrative Copy', {
            'fields': ('specializations_title', 'sub_content')
        }),
        ('Left Banner Image Asset', {
            'fields': ('banner_image', 'image_detail_preview')
        }),
        ('Prerequisites Box Config', {
            'fields': ('prerequisite_title', 'prerequisite_overview')
        }),
        ('Action CTAs & Links', {
            'fields': ('apply_button_text', 'eligibility_button_text', 'syllabus_button_text', 'custom_syllabus_redirect_url')
        }),
        ('Display Control & Visibility', {
            'fields': ('display_order', 'is_active')
        }),
        SEO_FIELDSET,
    )

    def banner_thumbnail(self, obj):
        return self._render_thumbnail(obj.banner_image, height=45)
    banner_thumbnail.short_description = "Banner"

    def image_detail_preview(self, obj):
        return self._render_detail_preview(obj.banner_image, height=140)
    image_detail_preview.short_description = "Banner Preview"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        clear_all_cms_caches()


@admin.register(ProgramTitle)
class ProgramTitleAdmin(SingletonAdminMixin, admin.ModelAdmin):
    list_display = ('heading', 'sub_heading', 'created_at')
    inlines = [ProgramInline]
    fieldsets = (
        (None, {
            'fields': ('heading', 'sub_heading')
        }),
        SEO_FIELDSET,
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('program_items', 'isolated_showcase_cards')

# ==============================================================================
# 4. CAMPUS FACILITIES ADMINS
# ==============================================================================
class CampusFacilityInline(EducationAdminMixin, admin.TabularInline):
    model = CampusFacility
    extra = 1
    fields = ('image', 'facility_inline_thumbnail', 'created_at')
    readonly_fields = ('created_at', 'facility_inline_thumbnail')

    def facility_inline_thumbnail(self, obj):
        return self._render_thumbnail(obj.image, height=35)
    facility_inline_thumbnail.short_description = "Current Asset"


@admin.register(CampusTitle)
class CampusTitleAdmin(SingletonAdminMixin, admin.ModelAdmin):
    list_display = ('heading', 'sub_heading', 'created_at')
    inlines = [CampusFacilityInline]
    fieldsets = (
        (None, {
            'fields': ('heading', 'sub_heading')
        }),
        SEO_FIELDSET,
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('campus_items')


@admin.register(CampusFacility)
class CampusFacilityAdmin(EducationAdminMixin, admin.ModelAdmin):
    list_display = ('id', 'campus_title', 'facility_image_thumbnail', 'created_at')
    list_filter = ('campus_title', 'created_at')
    list_select_related = ('campus_title',)
    readonly_fields = ('created_at', 'facility_detail_preview')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        clear_all_cms_caches()

    def facility_image_thumbnail(self, obj):
        return self._render_thumbnail(obj.image, height=45)
    facility_image_thumbnail.short_description = "Thumbnail"

    def facility_detail_preview(self, obj):
        return self._render_detail_preview(obj.image, height=140)
    facility_detail_preview.short_description = "Facility Asset Preview"

# ==============================================================================
# 5. INSTITUTIONAL NEWS ADMINS
# ==============================================================================
class NewsEventInline(admin.TabularInline):
    model = NewsEvent
    extra = 1
    fields = ('date', 'heading', 'content', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(NewsTitle)
class NewsTitleAdmin(SingletonAdminMixin, admin.ModelAdmin):
    list_display = ('heading', 'sub_heading', 'created_at')
    inlines = [NewsEventInline]
    fieldsets = (
        (None, {
            'fields': ('heading', 'sub_heading')
        }),
        SEO_FIELDSET,
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('news_items')


@admin.register(NewsEvent)
class NewsEventAdmin(admin.ModelAdmin):
    list_display = ('heading', 'news_title', 'date', 'trimmed_content', 'created_at')
    list_filter = ('news_title', 'date', 'created_at')
    search_fields = ('heading', 'content')
    list_select_related = ('news_title',)
    readonly_fields = ('created_at',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        clear_all_cms_caches()

    def trimmed_content(self, obj):
        if obj.content and len(obj.content) > 75:
            return f"{obj.content[:72]}..."
        return obj.content or "-"
    trimmed_content.short_description = "Content"

# ==============================================================================
# 6. ADMISSIONS CRITERIA & CONFIGURATION ADMINS
# ==============================================================================
@admin.register(AdmissionContactDetail)
class AdmissionContactDetailAdmin(SingletonAdminMixin, admin.ModelAdmin):
    list_display = ('heading', 'sub_heading', 'mail_id', 'contact', 'created_at')
    readonly_fields = ('created_at',)


class AdmissionCriteriaInline(admin.TabularInline):
    model = AdmissionCriteria
    extra = 1
    fields = ('content', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(AdmissionDetailTitle)
class AdmissionDetailTitleAdmin(SingletonAdminMixin, admin.ModelAdmin):
    list_display = ('heading', 'sub_heading', 'sub_content', 'created_at')
    inlines = [AdmissionCriteriaInline]
    readonly_fields = ('created_at',)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('criteria_items')


@admin.register(AdmissionCriteria)
class AdmissionCriteriaAdmin(admin.ModelAdmin):
    list_display = ('content', 'admission_detail', 'created_at')
    list_filter = ('admission_detail', 'created_at')
    search_fields = ('content',)
    list_select_related = ('admission_detail',)
    readonly_fields = ('created_at',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        clear_all_cms_caches()

# ==============================================================================
# 7. FACULTY & STAFF DIRECTORY ADMINS
# ==============================================================================
class TeamMemberInline(nested_admin.NestedTabularInline):
    model = TeamMember
    extra = 1
    fields = ('name', 'profile_image', 'designation', 'message', 'created_at')
    readonly_fields = ('created_at',)


class TeamFacultyInline(nested_admin.NestedStackedInline):
    model = TeamFaculty
    extra = 1
    inlines = [TeamMemberInline]
    fields = ('heading', 'sub_heading', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(TeamTitle)
class TeamTitleAdmin(nested_admin.NestedModelAdmin, SingletonAdminMixin):
    list_display = ('heading', 'sub_heading', 'created_at')
    inlines = [TeamFacultyInline]
    fieldsets = (
        (None, {
            'fields': ('heading', 'sub_heading')
        }),
        SEO_FIELDSET,
    )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('faculty_items__member_items')


@admin.register(TeamFaculty)
class TeamFacultyAdmin(admin.ModelAdmin):
    list_display = ('heading', 'sub_heading', 'team_title', 'created_at')
    list_filter = ('team_title', 'created_at')
    search_fields = ('heading', 'sub_heading')
    list_select_related = ('team_title',)
    readonly_fields = ('created_at',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        clear_all_cms_caches()


@admin.register(TeamMember)
class TeamMemberAdmin(EducationAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'designation', 'faculty', 'member_thumbnail', 'created_at')
    list_filter = ('faculty__team_title', 'faculty', 'created_at')
    search_fields = ('name', 'designation', 'message')
    list_select_related = ('faculty__team_title', 'faculty')
    readonly_fields = ('created_at', 'photo_detail_preview')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        clear_all_cms_caches()

    def member_thumbnail(self, obj):
        return self._render_thumbnail(obj.profile_image, height=45)
    member_thumbnail.short_description = "Photo"

    def photo_detail_preview(self, obj):
        return self._render_detail_preview(obj.profile_image, height=130)
    photo_detail_preview.short_description = "Photo Preview"

# ==============================================================================
# 8. INQUIRY LOGS & ADMISSION FORM SUBMISSIONS
# ==============================================================================
@admin.register(ApplyJobDetail)
class ApplyJobDetailAdmin(SingletonAdminMixin, admin.ModelAdmin):
    list_display = ('heading', 'sub_heading', 'mail_id', 'contact', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'contact', 'city', 'created_at')
    list_filter = ('city', 'created_at')
    search_fields = ('name', 'email', 'contact', 'city', 'message')
    readonly_fields = ('created_at',)

    def has_add_permission(self, request):
        return False


@admin.register(ApplyCourse)
class ApplyCourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'email', 'contact', 'program', 'institution', 'created_at')
    list_filter = ('gender', 'program', 'created_at')
    search_fields = ('name', 'email', 'contact', 'institution', 'message')
    list_select_related = ('program',)
    readonly_fields = ('created_at',)

    def has_add_permission(self, request):
        return False


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('created_at',)


@admin.register(ApplyPosition)
class ApplyPositionAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'email', 'contact', 'position', 'resume_download_shortcut', 'created_at')
    list_filter = ('gender', 'position', 'created_at')
    search_fields = ('name', 'email', 'contact', 'message')
    list_select_related = ('position',)
    readonly_fields = ('created_at', 'resume_detail_preview')

    def has_add_permission(self, request):
        return False

    def resume_download_shortcut(self, obj):
        if obj.document:
            return mark_safe(f'<a href="{obj.document.url}" target="_blank" style="font-weight: bold; color: #009444;">Download CV</a>')
        return mark_safe('<span style="color: #a0aec0; font-style: italic;">No CV uploaded</span>')
    resume_download_shortcut.short_description = "Resume File"

    def resume_detail_preview(self, obj):
        if obj.document:
            return mark_safe(
                f'<div style="background: #f8fafc; padding: 10px; border: 1px solid #e2e8f0; border-radius: 4px; display: inline-block;">'
                f'<a href="{obj.document.url}" target="_blank" style="font-weight: bold; color: #009444; text-decoration: underline;">'
                f'Open Document / Download CV ({obj.document.name.split("/")[-1]})'
                f'</a>'
                f'</div>'
            )
        return mark_safe('<span style="color: #a0aec0; font-style: italic;">No document submitted</span>')
    resume_detail_preview.short_description = "Resume Preview"

# ==============================================================================
# 9. SUBMISSION FORM LANDING BANNERS
# ==============================================================================
@admin.register(ApplyForCourseBanner)
class ApplyForCourseBannerAdmin(EducationAdminMixin, SingletonAdminMixin, admin.ModelAdmin):
    list_display = ('heading', 'sub_heading', 'banner_thumbnail', 'created_at')
    readonly_fields = ('created_at', 'banner_detail_preview')
    fieldsets = (
        (None, {
            'fields': ('heading', 'sub_heading', 'image', 'banner_detail_preview')
        }),
        SEO_FIELDSET,
    )

    def banner_thumbnail(self, obj):
        return self._render_thumbnail(obj.image, height=45)
    banner_thumbnail.short_description = "Banner Image"

    def banner_detail_preview(self, obj):
        return self._render_detail_preview(obj.image, height=140)
    banner_detail_preview.short_description = "Banner Preview"


@admin.register(ApplyForPositionBanner)
class ApplyForPositionBannerAdmin(EducationAdminMixin, SingletonAdminMixin, admin.ModelAdmin):
    list_display = ('heading', 'sub_heading', 'banner_thumbnail', 'created_at')
    readonly_fields = ('created_at', 'banner_detail_preview')
    fieldsets = (
        (None, {
            'fields': ('heading', 'sub_heading', 'image', 'banner_detail_preview')
        }),
        SEO_FIELDSET,
    )

    def banner_thumbnail(self, obj):
        return self._render_thumbnail(obj.image, height=45)
    banner_thumbnail.short_description = "Banner Image"

    def banner_detail_preview(self, obj):
        return self._render_detail_preview(obj.image, height=140)
    banner_detail_preview.short_description = "Banner Preview"

# ==============================================================================
# 10. GLOBAL SYSTEM SETTINGS & FOOTER CONFIGURATION
# ==============================================================================
class FooterLinkInline(admin.TabularInline):
    model = FooterLink
    extra = 1
    fields = ('category', 'title', 'url', 'display_order', 'is_active', 'open_in_new_tab', 'created_at')
    readonly_fields = ('created_at',)
    ordering = ('category', 'display_order', '-created_at')


@admin.register(FooterConfig)
class FooterConfigAdmin(EducationAdminMixin, SingletonAdminMixin, admin.ModelAdmin):
    list_display = ('__str__', 'logo_thumbnail', 'trimmed_branding_description', 'created_at')
    readonly_fields = ('created_at', 'logo_detail_preview')
    inlines = [FooterLinkInline]
    fieldsets = (
        ('Branding & Corporate Identity', {
            'fields': ('logo', 'logo_detail_preview', 'branding_description'),
        }),
        ('Social Platforms Directories', {
            'fields': ('facebook_url', 'linkedin_url', 'instagram_url'),
        }),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        clear_all_cms_caches()

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        clear_all_cms_caches()

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('footer_links')

    def logo_thumbnail(self, obj):
        return self._render_thumbnail(obj.logo, height=45)
    logo_thumbnail.short_description = "Logo Thumbnail"

    def logo_detail_preview(self, obj):
        return self._render_detail_preview(obj.logo, height=130)
    logo_detail_preview.short_description = "Logo Preview"

    def trimmed_branding_description(self, obj):
        if obj.branding_description and len(obj.branding_description) > 75:
            return f"{obj.branding_description[:72]}..."
        return obj.branding_description or "-"
    trimmed_branding_description.short_description = "Branding Description"


@admin.register(FooterLink)
class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'display_order', 'is_active', 'open_in_new_tab', 'footer_config', 'created_at')
    list_filter = ('category', 'is_active', 'open_in_new_tab', 'footer_config', 'created_at')
    search_fields = ('title', 'url')
    list_editable = ('category', 'display_order', 'is_active', 'open_in_new_tab')
    readonly_fields = ('created_at',)
    list_select_related = ('footer_config',)
    ordering = ('category', 'display_order', '-created_at')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        clear_all_cms_caches()

# ==============================================================================
# 11. CMS FAQ & DYNAMIC PAGE CONTENT ADMINS
# ==============================================================================
class FAQItemInline(admin.TabularInline):
    model = FAQItem
    extra = 1
    fields = ('question', 'answer', 'is_active', 'display_order', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'display_order', 'created_at')
    list_editable = ('display_order',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [FAQItemInline]
    ordering = ('display_order', '-created_at')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        clear_all_cms_caches()

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('faq_items')


@admin.register(FAQItem)
class FAQItemAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'display_order', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('question', 'answer')
    list_editable = ('display_order', 'is_active')
    autocomplete_fields = ['category']
    readonly_fields = ('created_at',)
    list_select_related = ('category',)
    ordering = ('category', 'display_order', '-created_at')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        clear_all_cms_caches()


@admin.register(DynamicPageContent)
class DynamicPageContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'page_key', 'subtitle', 'is_active', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('title', 'page_key', 'subtitle')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('page_key', 'title', 'subtitle', 'content_json', 'is_active')
        }),
        SEO_FIELDSET,
        ('System Metadata', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        clear_all_cms_caches()

# ==============================================================================
# 12. DYNAMIC NOTIFICATION & SMTP CONFIGURATION ADMIN
# ==============================================================================
# ==============================================================================
# ENHANCEMENT 1 (admin.py):
# Custom ModelForm that auto-generates a warning banner shown to admins
# whenever (a) no email_logo is uploaded, or (b) a previously-uploaded SVG
# is still in place despite the new raster-only restriction.
# This is purely UX — no functional change, just clearer admin feedback.
# ==============================================================================
def _detect_email_logo_issue(instance):
    """
    Returns a mark_safe-formatted warning HTML string if there's a known
    issue with the email logo configuration. Returns empty string if all OK.
    """
    warnings = []

    # Check 1: No email_logo at all
    if not instance.email_logo:
        warnings.append(
            "<strong>No email logo configured.</strong> Outgoing emails will fall back to the "
            "site header logo or footer logo (if raster) and ultimately to a remote PNG. "
            "Upload a dedicated PNG/JPG here for the most reliable email rendering."
        )

    # Check 2: Previously uploaded file is SVG (still present in storage
    # from before the raster-only restriction was applied). The new
    # validator blocks new SVG uploads but cannot retroactively remove
    # existing ones — admins must re-upload as PNG.
    if instance.email_logo and instance.email_logo.name:
        filename_lc = instance.email_logo.name.lower()
        if filename_lc.endswith('.svg'):
            warnings.append(
                "<strong>Email logo is SVG.</strong> Most email clients (Gmail web, legacy "
                "Outlook desktop) cannot render inline SVG. Please re-export your logo as "
                "PNG or JPG and re-upload here. Clear this field first, then upload the "
                "raster version."
            )

    if not warnings:
        return mark_safe("")

    items_html = "".join(f"<li style='margin-bottom:4px;'>{w}</li>" for w in warnings)
    return mark_safe(
        "<div style='background:#fef3c7;border:1px solid #f59e0b;color:#92400e;"
        "padding:12px 16px;border-radius:6px;margin-bottom:14px;'>"
        "<p style='margin:0 0 8px 0;font-weight:700;font-size:13px;'>"
        "⚠ Email Logo Configuration Notice</p>"
        f"<ul style='margin:0;padding-left:20px;font-size:12px;line-height:1.5;'>{items_html}</ul>"
        "</div>"
    )


class NotificationSettingForm(forms.ModelForm):
    smtp_password = forms.CharField(
        widget=forms.PasswordInput(render_value=True),
        required=False,
        label="SMTP Password / App Credential",
        help_text="Encrypted password or app-specific key used for SMTP handshakes."
    )

    class Meta:
        model = NotificationSetting
        fields = '__all__'

        # ENHANCEMENT 2 (admin.py):
        # Add a clear helper_text override on the email_logo form field
        # so admin users immediately understand the raster-only requirement,
        # the reason, and the recommended format/dimensions. Django's
        # built-in `email_logo` form field still inherits the
        # validate_email_image_file validator from models.py automatically.
        help_texts = {
            'email_logo': (
                "Upload a RASTER image (JPG, JPEG, PNG, or WEBP only — SVG is rejected). "
                "Recommended: PNG with transparent background, 200–300px wide. "
                "Used as an inline CID image at the top of all outgoing emails. "
                "Maximum file size: 10MB."
            ),
        }


@admin.register(NotificationSetting)
class NotificationSettingAdmin(EducationAdminMixin, SingletonAdminMixin, admin.ModelAdmin):
    form = NotificationSettingForm
    list_display = (
        'name', 'provider', 'smtp_host', 'smtp_port',
        'primary_admin_email', 'is_active', 'created_at'
    )
    readonly_fields = ('created_at', 'email_logo_preview', 'email_logo_warning_banner')

    fieldsets = (
        ('General Profile & Status', {
            'fields': ('name', 'is_active')
        }),
        ('Dedicated Email Branding & Logo', {
            'fields': (
                'email_logo_warning_banner',
                'email_logo', 'email_logo_preview',
                'email_header_bg_color', 'email_footer_text', 'email_footer_address'
            ),
            # ENHANCEMENT 3 (admin.py):
            # Fieldset description updated to inform admins upfront WHY only
            # raster formats work, before they even try to upload an SVG.
            'description': (
                "Upload a RASTER logo (PNG/JPG/JPEG/WEBP) specifically formatted for email headers. "
                "SVG is NOT supported because most email clients (Gmail web, Outlook desktop) "
                "cannot render inline SVG reliably. Recommended size: PNG with transparent "
                "background, ~200–300px wide. The site header logo and footer logo are used "
                "as automatic fallbacks if this dedicated email logo is not provided."
            )
        }),
        ('Provider & SMTP Server Settings', {
            'fields': ('provider', 'smtp_host', 'smtp_port', 'encryption', 'timeout')
        }),
        ('Authentication Credentials', {
            'fields': ('smtp_username', 'smtp_password')
        }),
        ('Default Sender Identity', {
            'fields': ('default_from_email', 'default_sender_name')
        }),
        ('Admin Notification Recipients', {
            'fields': ('primary_admin_email', 'secondary_admin_email'),
            'description': 'These college email addresses will receive alerts whenever a student, job seeker, or inquirer submits a form.'
        }),
        ('Notification Rules & Triggers', {
            'fields': ('send_applicant_confirmation', 'send_admin_notification')
        }),
        ('Customizable Course Application Email Templates', {
            'classes': ('collapse',),
            'fields': ('course_app_subject', 'course_app_applicant_body'),
            'description': 'Available dynamic placeholders: {applicant_name}, {program_name}, {contact}, {email}, {institution}'
        }),
        ('Customizable Job Application Email Templates', {
            'classes': ('collapse',),
            'fields': ('job_app_subject', 'job_app_applicant_body'),
            'description': 'Available dynamic placeholders: {applicant_name}, {position_name}, {contact}, {email}'
        }),
        ('Customizable Contact Inquiry Email Templates', {
            'classes': ('collapse',),
            'fields': ('contact_subject', 'contact_applicant_body'),
            'description': 'Available dynamic placeholders: {applicant_name}, {city}, {contact}, {email}'
        }),
        ('Applicant "What Happens Next?" Callout Card', {
            'classes': ('collapse',),
            'fields': ('next_steps_heading', 'next_steps_body'),
            'description': 'Customize the info box shown to students after submitting a course application.'
        }),
    )

    def email_logo_preview(self, obj):
        return self._render_detail_preview(obj.email_logo, height=80)
    email_logo_preview.short_description = "Email Logo Preview"

    def email_logo_warning_banner(self, obj):
        """
        Inline warning banner ABOVE the email_logo field that highlights
        raster requirement violations or missing logo configurations.
        Pure UX enhancement — no functional change to email rendering logic.
        """
        return _detect_email_logo_issue(obj)
    email_logo_warning_banner.short_description = "Configuration Health Check"