import csv
from django.contrib import admin
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from django.utils.timezone import now
from django.core.cache import cache

from home.admin import SingletonAdminMixin, EducationAdminMixin, SEO_FIELDSET
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

def clear_training_cms_caches():
    """Clears cached payloads for immediate frontend synchronization."""
    try:
        cache.delete('aiems_training_content_payload')
        cache.delete('aiems_home_content_payload')
    except Exception:
        pass

# ==============================================================================
# INLINE CONFIGURATION EDITORS
# ==============================================================================
class TrainingCurriculumModuleInline(admin.TabularInline):
    model = TrainingCurriculumModule
    extra = 7
    fields = ('title', 'icon_class', 'description', 'display_order', 'is_active')
    ordering = ('display_order', 'id')

class TrainingTimeSlotInline(admin.TabularInline):
    model = TrainingTimeSlot
    extra = 4
    fields = ('time_range', 'slot_tag', 'display_order', 'is_active')
    ordering = ('display_order', 'id')

class TrainingSidebarPerkInline(admin.TabularInline):
    model = TrainingSidebarPerk
    extra = 4
    fields = ('title', 'icon_class', 'display_order')
    ordering = ('display_order', 'id')

class TrainingStreamOptionInline(admin.TabularInline):
    model = TrainingStreamOption
    extra = 4
    fields = ('name', 'display_order', 'is_active')
    ordering = ('display_order', 'id')

class TrainingTimeframeOptionInline(admin.TabularInline):
    model = TrainingTimeframeOption
    extra = 3
    fields = ('name', 'display_order', 'is_active')
    ordering = ('display_order', 'id')

class TrainingDeliveryModeInline(admin.TabularInline):
    model = TrainingDeliveryMode
    extra = 2
    fields = ('name', 'display_order', 'is_active')
    ordering = ('display_order', 'id')

class TrainingExperienceLevelInline(admin.TabularInline):
    model = TrainingExperienceLevel
    extra = 3
    fields = ('name', 'display_order', 'is_active')
    ordering = ('display_order', 'id')

# ==============================================================================
# TRAINING CMS PAGE BANNER ADMIN
# ==============================================================================
@admin.register(TrainingPageBanner)
class TrainingPageBannerAdmin(EducationAdminMixin, SingletonAdminMixin, admin.ModelAdmin):
    list_display = ('heading', 'badge_text', 'banner_thumbnail', 'created_at')
    readonly_fields = ('created_at', 'image_detail_preview')
    inlines = [
        TrainingCurriculumModuleInline,
        TrainingTimeSlotInline,
        TrainingSidebarPerkInline,
        TrainingStreamOptionInline,
        TrainingTimeframeOptionInline,
        TrainingDeliveryModeInline,
        TrainingExperienceLevelInline,
    ]
    fieldsets = (
        ('Section Headlines & Badges', {
            'fields': ('badge_text', 'heading', 'sub_heading')
        }),
        ('Action CTA Buttons', {
            'fields': ('primary_btn_text', 'primary_btn_url')
        }),
        ('Hero Background Image Asset', {
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

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        clear_training_cms_caches()

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        clear_training_cms_caches()

# ==============================================================================
# CAPTURED LEADS ADMIN WITH DIRECT CSV EXPORT ACTION
# ==============================================================================
@admin.register(TrainingApplicationLead)
class TrainingApplicationLeadAdmin(admin.ModelAdmin):
    list_display = (
        'ref_id', 'full_name', 'gender', 'phone', 
        'email', 'academic_stream', 'timeframe', 'time_slot', 'created_at'
    )
    list_filter = ('timeframe', 'time_slot', 'academic_stream', 'gender', 'training_mode', 'created_at')
    search_fields = ('ref_id', 'full_name', 'phone', 'whatsapp', 'email', 'institution', 'timeframe')
    readonly_fields = (
        'ref_id', 'full_name', 'gender', 'phone', 'whatsapp',
        'email', 'academic_stream', 'institution', 'selected_modules',
        'timeframe', 'time_slot', 'training_mode', 'experience_level', 'learning_goal', 'created_at'
    )
    actions = ['export_leads_as_csv']
    ordering = ('-created_at',)

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    @admin.action(description="Export Selected Leads to CSV Spreadsheet")
    def export_leads_as_csv(self, request, queryset):
        field_names = [
            'ref_id', 'full_name', 'gender', 'phone', 'whatsapp',
            'email', 'academic_stream', 'institution', 'timeframe',
            'time_slot', 'training_mode', 'experience_level',
            'selected_modules', 'learning_goal', 'created_at'
        ]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename=AIEMS_Training_Leads_{now().strftime("%Y%m%d_%H%M%S")}.csv'
        writer = csv.writer(response)

        writer.writerow([field.replace('_', ' ').upper() for field in field_names])
        for obj in queryset:
            row = []
            for field in field_names:
                val = getattr(obj, field)
                if isinstance(val, list):
                    val = "; ".join(str(item) for item in val)
                row.append(str(val))
            writer.writerow(row)

        return response