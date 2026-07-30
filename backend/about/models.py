import os
import uuid
from django.db import models
from django.utils.timezone import now
from django.core.validators import EmailValidator

from home.models import (
    SEOMetadataMixin,
    validate_image_file,
    phone_validator
)

# ==============================================================================
# SECURE FILE UTILITIES & PATH GENERATORS
# ==============================================================================
def secure_about_file_rename(instance, filename, folder_name):
    """
    Generates a unique, non-guessable UUID filename preserving the original extension.
    Prevents file naming collisions and directory traversal security exploits.
    """
    ext = os.path.splitext(filename)[1].lower()
    unique_filename = f"{uuid.uuid4()}{ext}"
    return os.path.join(folder_name, unique_filename)

def about_banner_path(instance, filename):
    return secure_about_file_rename(instance, filename, 'about/banners')

def about_icon_path(instance, filename):
    return secure_about_file_rename(instance, filename, 'about/icons')

def about_user_path(instance, filename):
    return secure_about_file_rename(instance, filename, 'about/users')

def about_facility_path(instance, filename):
    return secure_about_file_rename(instance, filename, 'about/facilities')

# ==============================================================================
# CONTENT MANAGEMENT SYSTEM (CMS) MODELS FOR ABOUT US PAGE
# ==============================================================================
class TopBanner(SEOMetadataMixin, models.Model):
    badge_text = models.CharField(
        max_length=255,
        default="",
        verbose_name="Top Badge Label"
    )
    heading = models.CharField(
        max_length=255,
        default="",
        verbose_name="Main Heading"
    )
    sub_heading = models.TextField(
        default="",
        verbose_name="Sub Heading"
    )
    image = models.ImageField(
        upload_to=about_banner_path, 
        validators=[validate_image_file],
        blank=True,
        null=True,
        verbose_name="Hero Background Image"
    )
    primary_btn_text = models.CharField(
        max_length=100,
        default="",
        verbose_name="Primary CTA Button Text"
    )
    primary_btn_url = models.CharField(
        max_length=255,
        default="#about-intro",
        verbose_name="Primary CTA Button Link"
    )
    secondary_btn_text = models.CharField(
        max_length=100,
        default="",
        verbose_name="Secondary CTA Button Text"
    )
    secondary_btn_url = models.CharField(
        max_length=255,
        default="#vision-mission",
        verbose_name="Secondary CTA Button Link"
    )
    created_at = models.DateTimeField(default=now, verbose_name="Created At", db_index=True)

    class Meta:
        verbose_name = "Top Hero Banner"
        verbose_name_plural = "Top Hero Banners"
        ordering = ['-created_at']

    def __str__(self):
        return self.heading or "About Top Hero Banner"


class AboutBanner(models.Model):
    badge_text = models.CharField(
        max_length=255,
        default="",
        verbose_name="Section Badge Label"
    )
    heading = models.CharField(
        max_length=255,
        default="",
        verbose_name="Main Title"
    )
    content_paragraph_1 = models.TextField(
        default="",
        verbose_name="First Narrative Paragraph"
    )
    content_paragraph_2 = models.TextField(
        default="",
        verbose_name="Second Narrative Paragraph"
    )
    main_image = models.ImageField(
        upload_to=about_banner_path,
        blank=True,
        null=True,
        validators=[validate_image_file],
        verbose_name="Executive Photo (Collage Main Image)"
    )
    charter_badge_title = models.CharField(
        max_length=100,
        default="",
        verbose_name="Charter Badge Small Title"
    )
    charter_badge_subtitle = models.CharField(
        max_length=150,
        default="",
        verbose_name="Charter Badge Headline"
    )
    charter_badge_degree = models.CharField(
        max_length=150,
        default="",
        verbose_name="Charter Badge Subtext"
    )
    created_at = models.DateTimeField(default=now, verbose_name="Created At", db_index=True)

    class Meta:
        verbose_name = "Executive Manifesto (About Intro)"
        verbose_name_plural = "Executive Manifestos"
        ordering = ['-created_at']

    def __str__(self):
        return self.heading or "About Manifesto Section"


class AboutManifestoDifferentiator(models.Model):
    about_banner = models.ForeignKey(
        AboutBanner,
        related_name="differentiators",
        on_delete=models.CASCADE,
        verbose_name="Manifesto Parent"
    )
    icon_class = models.CharField(
        max_length=100,
        default="fa-solid fa-graduation-cap",
        verbose_name="FontAwesome Icon Class"
    )
    title = models.CharField(max_length=255, verbose_name="Differentiator Title")
    description = models.TextField(verbose_name="Differentiator Description")
    display_order = models.PositiveIntegerField(default=0, verbose_name="Display Order")

    class Meta:
        verbose_name = "Manifesto Differentiator Pill"
        verbose_name_plural = "Manifesto Differentiator Pills"
        ordering = ['display_order', 'id']

    def __str__(self):
        return self.title


class AboutVisionTitle(SEOMetadataMixin, models.Model):
    badge_text = models.CharField(
        max_length=255,
        default="",
        verbose_name="Section Badge Label"
    )
    heading = models.CharField(
        max_length=255,
        default="",
        verbose_name="Section Heading"
    )
    sub_heading = models.TextField(
        default="",
        verbose_name="Section Subheading"
    )
    created_at = models.DateTimeField(default=now, verbose_name="Created At", db_index=True)

    class Meta:
        verbose_name = "Vision & Mission Section Title"
        verbose_name_plural = "Vision & Mission Section Titles"
        ordering = ['-created_at']

    def __str__(self):
        return self.heading or "Vision & Mission Section"


class AboutVisionBanner(models.Model):
    BORDER_COLOR_CHOICES = (
        ('border-brandPrimary', 'Brand Primary (Green)'),
        ('border-brandSecondary', 'Brand Secondary (Navy Blue)'),
        ('border-brandAccent', 'Brand Accent (Cyan)'),
    )

    about_vision = models.ForeignKey(
        AboutVisionTitle, 
        related_name="about_vision_items", 
        on_delete=models.CASCADE,
        verbose_name="Vision Section Parent"
    )
    heading = models.CharField(max_length=255, verbose_name="Pillar Title (e.g. Our Vision)")
    content = models.TextField(default='', blank=True, verbose_name="Pillar Narrative Copy")
    icon_class = models.CharField(
        max_length=100,
        default="fa-solid fa-eye",
        verbose_name="FontAwesome Icon Class"
    )
    border_color_class = models.CharField(
        max_length=50,
        choices=BORDER_COLOR_CHOICES,
        default='border-brandPrimary',
        verbose_name="Card Accent Left Border Color"
    )
    display_order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    created_at = models.DateTimeField(default=now, verbose_name="Created At", db_index=True)

    class Meta:
        verbose_name = "Vision / Mission / Goal Pillar Card"
        verbose_name_plural = "Vision / Mission / Goal Pillar Cards"
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return f"{self.about_vision.heading if self.about_vision else ''} -> {self.heading}"


class AboutVisionItems(models.Model):
    about_title = models.ForeignKey(
        AboutVisionBanner, 
        related_name="items", 
        on_delete=models.CASCADE,
        verbose_name="Pillar Card Parent"
    )
    content = models.TextField(default='', blank=True, verbose_name="Checklist Bullet Detail")
    created_at = models.DateTimeField(default=now, verbose_name="Created At", db_index=True)

    class Meta:
        verbose_name = "Pillar Checklist Bullet"
        verbose_name_plural = "Pillar Checklist Bullets"
        ordering = ['id']

    def __str__(self):
        return self.content[:50] if self.content else "Checklist Detail"


class CoreValuesTitle(SEOMetadataMixin, models.Model):
    heading = models.CharField(
        max_length=255,
        default="",
        verbose_name="Heading"
    )
    sub_heading = models.TextField(
        default="",
        verbose_name="Sub Heading"
    )
    image = models.ImageField(
        upload_to=about_icon_path, 
        blank=True, 
        null=True, 
        validators=[validate_image_file],
        verbose_name="Section Background/Icon"
    )
    created_at = models.DateTimeField(default=now, verbose_name="Created At", db_index=True)

    class Meta:
        verbose_name = "Core Values Section Title"
        verbose_name_plural = "Core Values Section Titles"
        ordering = ['-created_at']

    def __str__(self):
        return self.heading or "Core Values Section Title"


class CoreValuesBanner(models.Model):
    core_title = models.ForeignKey(
        CoreValuesTitle, 
        related_name="core_items", 
        on_delete=models.CASCADE,
        verbose_name="Core Values Title Group"
    )
    heading = models.CharField(max_length=255, verbose_name="Value Name (e.g. Innovation)")
    content = models.TextField(default='', blank=True, verbose_name="Value Description")
    icon_class = models.CharField(
        max_length=100,
        default="fa-solid fa-laptop-code",
        verbose_name="FontAwesome Icon Class"
    )
    image = models.ImageField(
        upload_to=about_icon_path, 
        blank=True, 
        null=True, 
        validators=[validate_image_file],
        verbose_name="Value Item Custom Icon Image"
    )
    display_order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    created_at = models.DateTimeField(default=now, verbose_name="Created At", db_index=True)

    class Meta:
        verbose_name = "Core Value Item"
        verbose_name_plural = "Core Value Items"
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return f"{self.core_title.heading if self.core_title else ''} -> {self.heading}"


class AboutMetric(models.Model):
    """
    Stores numerical parameters for the Dark Metric Counters section on the About Us page.
    """
    target_number = models.IntegerField(default=0, verbose_name="Target Number for Animated Counter")
    prefix = models.CharField(max_length=20, blank=True, default="", verbose_name="Value Prefix (e.g. '1:')")
    suffix = models.CharField(max_length=20, blank=True, default="", verbose_name="Value Suffix (e.g. 'Yr', '%', '+')")
    label = models.CharField(max_length=255, verbose_name="Primary Metric Label")
    sub_label = models.CharField(max_length=255, blank=True, default="", verbose_name="Sub Label")
    display_order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Institutional Distinction Metric"
        verbose_name_plural = "Institutional Distinction Metrics"
        ordering = ['display_order', 'id']

    def __str__(self):
        return f"{self.prefix}{self.target_number}{self.suffix} - {self.label}"


class LeadershipTitle(SEOMetadataMixin, models.Model):
    badge_text = models.CharField(
        max_length=255,
        default="",
        verbose_name="Section Badge Label"
    )
    heading = models.CharField(
        max_length=255,
        default="",
        verbose_name="Heading"
    )
    sub_heading = models.TextField(
        default="",
        verbose_name="Sub Heading"
    )
    created_at = models.DateTimeField(default=now, verbose_name="Created At", db_index=True)

    class Meta:
        verbose_name = "Leadership Section Title"
        verbose_name_plural = "Leadership Section Titles"
        ordering = ['-created_at']

    def __str__(self):
        return self.heading or "Leadership Section Title"


class LeadershipBanner(models.Model):
    leadership = models.ForeignKey(
        LeadershipTitle, 
        related_name="leadership_items", 
        on_delete=models.CASCADE,
        verbose_name="Leadership Section Parent"
    )
    heading = models.CharField(max_length=255, verbose_name="Full Name / Executive Title")
    designation = models.CharField(max_length=255, default="", verbose_name="Designation Badge")
    content = models.TextField(default='', blank=True, verbose_name="Executive Statement / Quote Bio")
    image = models.ImageField(
        upload_to=about_user_path, 
        blank=True, 
        null=True, 
        validators=[validate_image_file],
        verbose_name="Profile Portrait"
    )
    display_order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    created_at = models.DateTimeField(default=now, verbose_name="Created At", db_index=True)

    class Meta:
        verbose_name = "Leadership Profile"
        verbose_name_plural = "Leadership Profiles"
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return f"{self.leadership.heading if self.leadership else ''} -> {self.heading}"


class CampusTitle(SEOMetadataMixin, models.Model):
    badge_text = models.CharField(
        max_length=255,
        default="",
        verbose_name="Section Badge Label"
    )
    heading = models.CharField(
        max_length=255,
        default="",
        verbose_name="Heading"
    )
    sub_heading = models.TextField(
        default="",
        verbose_name="Sub Heading"
    )
    created_at = models.DateTimeField(default=now, verbose_name="Created At", db_index=True)

    class Meta:
        verbose_name = "Campus Ecosystem Section Title"
        verbose_name_plural = "Campus Ecosystem Section Titles"
        ordering = ['-created_at']

    def __str__(self):
        return self.heading or "Campus Ecosystem Section Title"


class CampusOverview(models.Model):
    BENTO_SPAN_CHOICES = (
        ('md:col-span-8', 'Wide Card (8 Columns)'),
        ('md:col-span-4', 'Standard Card (4 Columns)'),
        ('md:col-span-12', 'Full Width (12 Columns)'),
    )

    campus_title = models.ForeignKey(
        CampusTitle, 
        related_name="campus_items", 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True,
        verbose_name="Campus Section Parent"
    )
    category_badge = models.CharField(max_length=100, default="", verbose_name="Category Badge")
    title = models.CharField(max_length=255, default="", verbose_name="Facility Title")
    description = models.TextField(
        default="",
        verbose_name="Facility Description"
    )
    icon_class = models.CharField(max_length=100, default="fa-solid fa-chalkboard-user", verbose_name="FontAwesome Icon Class")
    image = models.ImageField(
        upload_to=about_facility_path, 
        blank=True, 
        null=True, 
        validators=[validate_image_file],
        verbose_name="Background / Facility Image"
    )
    bento_span_class = models.CharField(
        max_length=50,
        choices=BENTO_SPAN_CHOICES,
        default='md:col-span-4',
        verbose_name="Bento Grid Column Span"
    )
    display_order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    created_at = models.DateTimeField(default=now, verbose_name="Created At", db_index=True)

    class Meta:
        verbose_name = "Learning Ecosystem Bento Facility"
        verbose_name_plural = "Learning Ecosystem Bento Facilities"
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return self.title or "Campus Facility Item"


class VisionResearchTitle(SEOMetadataMixin, models.Model):
    badge_text = models.CharField(
        max_length=255,
        default="",
        verbose_name="Section Badge Label"
    )
    heading = models.CharField(
        max_length=255,
        default="",
        verbose_name="Heading"
    )
    created_at = models.DateTimeField(default=now, verbose_name="Created At", db_index=True)

    class Meta:
        verbose_name = "Research & Innovation Section Title"
        verbose_name_plural = "Research & Innovation Section Titles"
        ordering = ['-created_at']

    def __str__(self):
        return self.heading or "Research Section Title"


class VisionResearchBanner(models.Model):
    vision_research = models.ForeignKey(
        VisionResearchTitle, 
        related_name="vision_research_items", 
        on_delete=models.CASCADE,
        verbose_name="Research Section Parent"
    )
    heading = models.CharField(max_length=255, verbose_name="R&D Focus Title")
    content = models.TextField(default='', blank=True, verbose_name="R&D Focus Description")
    display_order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    created_at = models.DateTimeField(default=now, verbose_name="Created At", db_index=True)

    class Meta:
        verbose_name = "Research & Innovation Pillar"
        verbose_name_plural = "Research & Innovation Pillars"
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return f"{self.vision_research.heading if self.vision_research else ''} -> {self.heading}"


class AchievementTitle(SEOMetadataMixin, models.Model):
    heading = models.CharField(max_length=255, verbose_name="Heading")
    created_at = models.DateTimeField(default=now, verbose_name="Created At", db_index=True)

    class Meta:
        verbose_name = "Achievement Section Title"
        verbose_name_plural = "Achievement Section Titles"
        ordering = ['-created_at']

    def __str__(self):
        return self.heading or "Achievement Section Title"


class AchievementBanner(models.Model):
    achievement = models.ForeignKey(
        AchievementTitle, 
        related_name="achievement_items", 
        on_delete=models.CASCADE,
        verbose_name="Achievement Title Group"
    )
    heading = models.CharField(max_length=255, verbose_name="Heading")
    content = models.TextField(default='', blank=True, verbose_name="Content")
    created_at = models.DateTimeField(default=now, verbose_name="Created At", db_index=True)

    class Meta:
        verbose_name = "Achievement Record"
        verbose_name_plural = "Achievement Records"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.achievement.heading if self.achievement else ''} -> {self.heading}"


class LearnMoreContact(models.Model):
    heading = models.CharField(
        max_length=255,
        default="",
        verbose_name="Headline"
    )
    sub_heading = models.TextField(
        default="",
        verbose_name="Sub Heading"
    )
    mail_id = models.CharField(
        max_length=255,
        default="",
        validators=[EmailValidator(message="Please provide a valid institutional email address.")],
        verbose_name="Inquiry Email Address"
    )
    contact = models.CharField(
        max_length=50, 
        default="",
        validators=[phone_validator], 
        verbose_name="Counseling Hotline / Contact"
    )
    button_text = models.CharField(
        max_length=100,
        default="",
        verbose_name="CTA Button Text"
    )
    button_url = models.CharField(
        max_length=255,
        default="/contact-us",
        verbose_name="CTA Button Link"
    )
    created_at = models.DateTimeField(default=now, verbose_name="Created At", db_index=True)

    class Meta:
        verbose_name = "Learn More Contact Information"
        verbose_name_plural = "Learn More Contact Information"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.heading} ({self.mail_id})"

# Retained backward-compatible alias
LearMoreContact = LearnMoreContact