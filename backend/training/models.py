import os
import uuid
import random
from django.db import models
from django.utils.timezone import now
from django.core.validators import EmailValidator

from home.models import (
    SEOMetadataMixin,
    validate_image_file,
    phone_validator,
    secure_file_rename
)
from home import choices

# ==============================================================================
# SECURE FILE UTILITIES & PATH GENERATORS
# ==============================================================================
def training_banner_path(instance, filename):
    return secure_file_rename(instance, filename, 'training/banners')

def generate_training_ref_id():
    """Generates an institutional reference ID format: AIEMS-TRN-XXXX"""
    random_num = random.randint(1000, 9999)
    return f"AIEMS-TRN-{random_num}"

# ==============================================================================
# CMS PAGE LAYOUT & CURRICULUM CONFIGURATION MODELS
# ==============================================================================
class TrainingPageBanner(SEOMetadataMixin, models.Model):
    badge_text = models.CharField(
        max_length=255,
        default="Zero Coding or Technical Background Required",
        verbose_name="Top Hero Badge Label"
    )
    heading = models.CharField(
        max_length=255,
        default="Bridge Into Tech: Practical IT & AI Training for Non-Tech Students",
        verbose_name="Main Headline"
    )
    sub_heading = models.TextField(
        default="Tailored exclusively for Management, Humanities, Arts, Education, and Law students. Master modern AI tools, coding logic, web essentials, cybersecurity, and cloud workspace through 100% hands-on lab sessions at AIEMS Bardibas.",
        verbose_name="Hero Narrative Subtext"
    )
    image = models.ImageField(
        upload_to=training_banner_path,
        validators=[validate_image_file],
        blank=True,
        null=True,
        verbose_name="Hero Background Image"
    )
    primary_btn_text = models.CharField(
        max_length=100,
        default="Reserve Your Seat",
        verbose_name="Primary CTA Button Text"
    )
    primary_btn_url = models.CharField(
        max_length=255,
        default="#trainingLeadForm",
        verbose_name="Primary CTA Link Target"
    )
    created_at = models.DateTimeField(default=now, verbose_name="Created At", db_index=True)

    class Meta:
        verbose_name = "Training Page Hero Banner"
        verbose_name_plural = "Training Page Hero Banners"
        ordering = ['-created_at']

    def __str__(self):
        return self.heading or "Training Page Hero Banner"


class TrainingCurriculumModule(models.Model):
    training_banner = models.ForeignKey(
        TrainingPageBanner,
        related_name="modules",
        on_delete=models.CASCADE,
        verbose_name="Parent Training Page"
    )
    title = models.CharField(
        max_length=255,
        verbose_name="Module Title (e.g., 1. AI Fundamentals)"
    )
    description = models.TextField(
        verbose_name="Module Description (Plain-English Summary)"
    )
    icon_class = models.CharField(
        max_length=100,
        default="fa-solid fa-brain",
        verbose_name="FontAwesome Icon Class"
    )
    display_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Display Order"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Module Active / Visible?"
    )
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Curriculum Module Track"
        verbose_name_plural = "Curriculum Module Tracks"
        ordering = ['display_order', 'id']

    def __str__(self):
        return self.title


class TrainingTimeSlot(models.Model):
    training_banner = models.ForeignKey(
        TrainingPageBanner,
        related_name="time_slots",
        on_delete=models.CASCADE,
        verbose_name="Parent Training Page"
    )
    time_range = models.CharField(
        max_length=100,
        verbose_name="Time Range Label (e.g., 4:00 PM - 5:00 PM)"
    )
    slot_tag = models.CharField(
        max_length=100,
        default="Evening Slot A",
        verbose_name="Slot Sub-Tag (e.g., Evening Slot A, Twilight Slot C)"
    )
    display_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Display Order"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Slot Active?"
    )
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Daily Evening Time Slot"
        verbose_name_plural = "Daily Evening Time Slots"
        ordering = ['display_order', 'id']

    def __str__(self):
        return f"{self.time_range} ({self.slot_tag})"


class TrainingSidebarPerk(models.Model):
    training_banner = models.ForeignKey(
        TrainingPageBanner,
        related_name="perks",
        on_delete=models.CASCADE,
        verbose_name="Parent Training Page"
    )
    title = models.CharField(
        max_length=255,
        verbose_name="Perk Headline (e.g., Dedicated Computer Lab Setup)"
    )
    icon_class = models.CharField(
        max_length=100,
        default="fa-solid fa-check",
        verbose_name="FontAwesome Icon Class"
    )
    display_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Display Order"
    )
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Sidebar Student Perk"
        verbose_name_plural = "Sidebar Student Perks"
        ordering = ['display_order', 'id']

    def __str__(self):
        return self.title


class TrainingStreamOption(models.Model):
    training_banner = models.ForeignKey(
        TrainingPageBanner,
        related_name="stream_options",
        on_delete=models.CASCADE,
        verbose_name="Parent Training Page"
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Academic Stream Option Name"
    )
    display_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Display Order"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Option Visible?"
    )
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Form Academic Stream Option"
        verbose_name_plural = "Form Academic Stream Options"
        ordering = ['display_order', 'id']

    def __str__(self):
        return self.name


class TrainingTimeframeOption(models.Model):
    """
    Configures available course duration options (e.g., 1 Month Crash Course, 
    3 Months Certificate Track, 6 Months Diploma Track) editable via CMS Admin.
    """
    training_banner = models.ForeignKey(
        TrainingPageBanner,
        related_name="timeframe_options",
        on_delete=models.CASCADE,
        verbose_name="Parent Training Page"
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Training Timeframe / Duration Option (e.g. '3 Months (Certificate Track)')"
    )
    display_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Display Order"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Option Active?"
    )
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Form Timeframe / Duration Option"
        verbose_name_plural = "Form Timeframe / Duration Options"
        ordering = ['display_order', 'id']

    def __str__(self):
        return self.name


class TrainingDeliveryMode(models.Model):
    training_banner = models.ForeignKey(
        TrainingPageBanner,
        related_name="delivery_modes",
        on_delete=models.CASCADE,
        verbose_name="Parent Training Page"
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Delivery Mode Option Name (e.g., Physical Lab at AIEMS Campus)"
    )
    display_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Display Order"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Option Active?"
    )
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Form Delivery Mode Option"
        verbose_name_plural = "Form Delivery Mode Options"
        ordering = ['display_order', 'id']

    def __str__(self):
        return self.name


class TrainingExperienceLevel(models.Model):
    training_banner = models.ForeignKey(
        TrainingPageBanner,
        related_name="experience_levels",
        on_delete=models.CASCADE,
        verbose_name="Parent Training Page"
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Computer Experience Level Name (e.g., Absolute Beginner)"
    )
    display_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Display Order"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Option Active?"
    )
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Form Experience Level Option"
        verbose_name_plural = "Form Experience Level Options"
        ordering = ['display_order', 'id']

    def __str__(self):
        return self.name

# ==============================================================================
# CAPTURED STUDENT LEADS REGISTRATION MODEL
# ==============================================================================
class TrainingApplicationLead(models.Model):
    ref_id = models.CharField(
        max_length=50,
        unique=True,
        default=generate_training_ref_id,
        db_index=True,
        verbose_name="Registration Reference ID"
    )
    full_name = models.CharField(
        max_length=255,
        verbose_name="Student Full Name"
    )
    gender = models.CharField(
        max_length=50,
        choices=choices.GenderChoices.choices,
        default=choices.GenderChoices.OTHER,
        verbose_name="Gender Identity"
    )
    phone = models.CharField(
        max_length=50,
        validators=[phone_validator],
        verbose_name="Mobile Phone Number"
    )
    whatsapp = models.CharField(
        max_length=50,
        blank=True,
        default="",
        verbose_name="WhatsApp Number"
    )
    email = models.CharField(
        max_length=255,
        validators=[EmailValidator()],
        verbose_name="Email Address"
    )
    academic_stream = models.CharField(
        max_length=255,
        verbose_name="Current Academic Background / Stream"
    )
    institution = models.CharField(
        max_length=255,
        verbose_name="Previous School / College / City"
    )
    selected_modules = models.JSONField(
        default=list,
        verbose_name="Enrolled Training Modules (JSON List)"
    )
    timeframe = models.CharField(
        max_length=150,
        default="3 Months (Certificate Track)",
        blank=True,
        verbose_name="Chosen Timeframe / Duration"
    )
    time_slot = models.CharField(
        max_length=100,
        verbose_name="Preferred Time Slot"
    )
    training_mode = models.CharField(
        max_length=150,
        default="Physical Lab at AIEMS Campus, Bardibas",
        verbose_name="Delivery Mode"
    )
    experience_level = models.CharField(
        max_length=150,
        blank=True,
        default="",
        verbose_name="Computer Comfort Level"
    )
    learning_goal = models.TextField(
        blank=True,
        default="",
        verbose_name="Specific Questions or Goals"
    )
    created_at = models.DateTimeField(
        default=now,
        db_index=True,
        verbose_name="Submitted Timestamp"
    )

    class Meta:
        verbose_name = "Captured Training Registration Lead"
        verbose_name_plural = "Captured Training Registration Leads"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['ref_id']),
            models.Index(fields=['phone']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"{self.ref_id} — {self.full_name} ({self.phone}) [{self.timeframe}]"