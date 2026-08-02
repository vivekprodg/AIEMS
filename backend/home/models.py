import os
import uuid
from django.db import models
from django.utils.timezone import now
from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError
from home import choices

# ==============================================================================
# SECURE FILE UTILITIES & VALIDATORS
# ==============================================================================
def secure_file_rename(instance, filename, folder_name):
    """
    Generates a unique, non-guessable UUID filename preserving the original extension.
    Prevents file naming collisions and directory traversal security exploits.
    """
    ext = os.path.splitext(filename)[1].lower()
    unique_filename = f"{uuid.uuid4()}{ext}"
    return os.path.join(folder_name, unique_filename)

def top_banner_image_path(instance, filename):
    return secure_file_rename(instance, filename, 'banners')

def popup_banner_image_path(instance, filename):
    return secure_file_rename(instance, filename, 'popups')

def about_banner_image_path(instance, filename):
    return secure_file_rename(instance, filename, 'about_banners')

def program_icon_path(instance, filename):
    return secure_file_rename(instance, filename, 'programs')

def campus_facility_path(instance, filename):
    return secure_file_rename(instance, filename, 'facilities')

def team_member_path(instance, filename):
    return secure_file_rename(instance, filename, 'teams')

def apply_position_resume_path(instance, filename):
    return secure_file_rename(instance, filename, 'resume')

def footer_logo_path(instance, filename):
    return secure_file_rename(instance, filename, 'footer')

def site_settings_logo_path(instance, filename):
    return secure_file_rename(instance, filename, 'site')

def email_logo_path(instance, filename):
    return secure_file_rename(instance, filename, 'email')

phone_validator = RegexValidator(
    regex=r'^\+?1?\d{7,20}$',
    message="Phone number must be valid format (7 to 20 digits, optionally starting with +)."
)

def validate_image_file(value):
    """
    Verifies that the uploaded asset is a valid web image and enforces a 10MB size limit.
    Accepts both raster (JPG, JPEG, PNG, WEBP) and vector (SVG) formats because
    the website itself renders SVG natively in modern browsers.

    For email-specific uploads use `validate_email_image_file` instead, since
    most email clients cannot render SVG reliably inside HTML emails.
    """
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.svg']
    if ext not in valid_extensions:
        raise ValidationError("Only image assets with extensions (JPG, JPEG, PNG, WEBP, SVG) are allowed.")

    max_size = 10 * 1024 * 1024  # 10MB
    if value.size > max_size:
        raise ValidationError("Image file size must not exceed 10MB.")


def validate_email_image_file(value):
    """
    Email-specific image validator.

    Restricts uploads to RASTER formats only (JPG, JPEG, PNG, WEBP).
    SVG is intentionally excluded because:
      - Gmail web strips <img> SVG references
      - Legacy Outlook desktop cannot render inline SVG
      - Apple Mail mobile / Gmail mobile only render SVG via base64 data URIs
        (handled at runtime by email_utils.py when this validator is bypassed,
        but the safest path is for admins to upload raster from the start).

    Enforces the same 10MB size cap as validate_image_file.
    """
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    if ext not in valid_extensions:
        raise ValidationError(
            "Email logos must be a raster image (JPG, JPEG, PNG, or WEBP). "
            "SVG is not supported by most email clients."
        )

    max_size = 10 * 1024 * 1024  # 10MB
    if value.size > max_size:
        raise ValidationError("Email logo file size must not exceed 10MB.")


def validate_document_file(value):
    """
    Ensures safe documentation submissions (PDF, DOC, DOCX) and enforces a 5MB limit.
    """
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.pdf', '.doc', '.docx']
    if ext not in valid_extensions:
        raise ValidationError("Only document formats (.pdf, .doc, .docx) are allowed.")

    max_size = 5 * 1024 * 1024  # 5MB
    if value.size > max_size:
        raise ValidationError("Document file size must not exceed 5MB.")

# ==============================================================================
# REUSABLE ENTERPRISE MIXINS
# ==============================================================================
class SEOMetadataMixin(models.Model):
    meta_title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Meta Title",
        help_text="Primary SEO title tag. Recommended length: 50-60 characters."
    )
    meta_description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Meta Description",
        help_text="SEO meta description tag. Recommended length: 150-160 characters."
    )
    meta_keywords = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Meta Keywords",
        help_text="Comma-separated keywords for search engine targeting."
    )
    structured_data = models.JSONField(
        blank=True,
        null=True,
        verbose_name="Structured Data (Schema.org / JSON-LD)",
        help_text="Valid JSON-LD block representing structured metadata schema."
    )

    class Meta:
        abstract = True

# ==============================================================================
# 1. CENTRALIZED SITE GLOBAL CONFIGURATION, NAVBAR & TICKERS
# ==============================================================================
class SiteGlobalSettings(SEOMetadataMixin, models.Model):
    site_title = models.CharField(
        max_length=255,
        default="AIEMS — Ankur Institute of Engineering and Management Studies",
        blank=True,
        null=True,
        verbose_name="Global Site Title"
    )
    primary_phone = models.CharField(
        max_length=50,
        default="9802113456",
        blank=True,
        null=True,
        validators=[phone_validator],
        verbose_name="Primary Hotline Number"
    )
    primary_email = models.CharField(
        max_length=255,
        default="info@aiems.edu.np",
        blank=True,
        null=True,
        validators=[EmailValidator()],
        verbose_name="Primary Inquiry Email"
    )
    location_address = models.CharField(
        max_length=255,
        default="Bardibas, Mahottari, Nepal",
        blank=True,
        null=True,
        verbose_name="Physical Campus Address"
    )
    map_iframe_url = models.TextField(
        default="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d14251.652199859013!2d85.8902!3d26.9806!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x39ec3f03a62886f3%3A0xc39cb7a32b62760!2sBardibas%2045700!5e0!3m2!1sen!2snp!4v1710000000000!5m2!1sen!2snp",
        blank=True,
        null=True,
        verbose_name="Google Map Embed URL"
    )
    logo = models.ImageField(
        upload_to=site_settings_logo_path,
        blank=True,
        null=True,
        validators=[validate_image_file],
        verbose_name="Main Site Header Logo"
    )
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Global Site Setting"
        verbose_name_plural = "Global Site Settings"
        ordering = ['-created_at']

    def __str__(self):
        return self.site_title or "Global Site Setting"


class NavbarLink(models.Model):
    site_settings = models.ForeignKey(
        SiteGlobalSettings,
        related_name="navbar_links",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Site Settings Parent"
    )
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name="Menu Link Label")
    url = models.CharField(max_length=500, blank=True, null=True, verbose_name="URL / Route Path")
    icon_class = models.CharField(
        max_length=100,
        default="fa-solid fa-house",
        blank=True,
        null=True,
        verbose_name="FontAwesome / Icon Class"
    )
    display_order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    is_active = models.BooleanField(default=True, verbose_name="Is Active?")
    is_button = models.BooleanField(default=False, verbose_name="Render as Action Button CTA?")
    open_in_new_tab = models.BooleanField(default=False, verbose_name="Open In New Tab?")
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Header Navigation Link"
        verbose_name_plural = "Header Navigation Links"
        ordering = ['display_order', '-created_at']
        indexes = [
            models.Index(fields=['display_order']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.title or 'Link'} ({self.url or ''})"


class AnnouncementTickerItem(models.Model):
    badge_label = models.CharField(
        max_length=100,
        default="Notice",
        blank=True,
        null=True,
        verbose_name="Badge Label"
    )
    text_content = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Announcement Headline Copy"
    )
    target_url = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default="",
        verbose_name="Action Link (Optional)"
    )
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    display_order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Announcement Ticker Item"
        verbose_name_plural = "Announcement Ticker Items"
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return f"{self.badge_label}: {self.text_content[:40] if self.text_content else ''}"


class EligibilityCalculatorConfig(models.Model):
    heading = models.CharField(
        max_length=255,
        default="BSc. CSIT Eligibility Calculator",
        blank=True,
        null=True,
        verbose_name="Calculator Heading"
    )
    sub_heading = models.TextField(
        default="Ensure your Grade 11 & 12 marks meet official university entrance rules before submitting your application.",
        blank=True,
        null=True,
        verbose_name="Sub Heading Description"
    )
    min_cgpa = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=2.20,
        blank=True,
        null=True,
        verbose_name="Minimum Required CGPA"
    )
    min_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=55.00,
        blank=True,
        null=True,
        verbose_name="Minimum Required Percentage (%)"
    )
    required_stream_text = models.CharField(
        max_length=255,
        default="Science Stream Mandatory: Physics & Mathematics background required in +2.",
        blank=True,
        null=True,
        verbose_name="Stream Requirement Label"
    )
    eligible_message = models.TextField(
        default="Congratulations! Your score meets the entrance requirements for BSc. CSIT.",
        blank=True,
        null=True,
        verbose_name="Pass/Eligible Message"
    )
    ineligible_message = models.TextField(
        default="Your score falls below the required threshold (minimum 2.2 CGPA or 55% in Grade 12 Science).",
        blank=True,
        null=True,
        verbose_name="Ineligible Message"
    )
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Eligibility Calculator Rule"
        verbose_name_plural = "Eligibility Calculator Rules"
        ordering = ['-created_at']

    def __str__(self):
        return self.heading or "Eligibility Calculator Rule"


class EligibilityStreamOption(models.Model):
    calculator_config = models.ForeignKey(
        EligibilityCalculatorConfig,
        related_name="stream_options",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Calculator Parent Config"
    )
    name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Stream / Program Option Name"
    )
    is_eligible = models.BooleanField(
        default=True,
        verbose_name="Is Eligible for Admission?"
    )
    display_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Display Order"
    )
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Academic Stream Option"
        verbose_name_plural = "Academic Stream Options"
        ordering = ['display_order', 'id']

    def __str__(self):
        return f"{self.name or 'Stream'} ({'Eligible' if self.is_eligible else 'Ineligible'})"


class HomepagePopupBanner(SEOMetadataMixin, models.Model):
    heading = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default="",
        verbose_name="Popup Banner Heading / Title"
    )
    sub_heading = models.TextField(
        blank=True,
        null=True,
        default="",
        verbose_name="Sub Heading / Short Description"
    )
    image = models.ImageField(
        upload_to=popup_banner_image_path,
        validators=[validate_image_file],
        blank=True,
        null=True,
        verbose_name="Popup Image / Flyer Asset (Flexible Size & Aspect Ratio)"
    )
    action_url = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        default="",
        verbose_name="Click-through CTA URL / Link"
    )
    button_text = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default="Apply Now",
        verbose_name="CTA Button Label"
    )
    show_cta_button = models.BooleanField(
        default=True,
        verbose_name="Show Action CTA Button?"
    )
    start_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Publish Start Timestamp (Optional)",
        help_text="If set, popup will only display on or after this timestamp."
    )
    end_date = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Publish Expiry Timestamp (Optional)",
        help_text="If set, popup will automatically stop displaying after this timestamp."
    )
    display_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Display Priority Order"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Active?"
    )
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Homepage Popup Banner"
        verbose_name_plural = "Homepage Popup Banners"
        ordering = ['display_order', '-created_at']
        indexes = [
            models.Index(fields=['display_order']),
            models.Index(fields=['is_active']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.heading or f"Homepage Popup Banner #{self.id}"

# ==============================================================================
# 2. CORE HOMEPAGE CMS MODELS WITH HERO TAGS, LANDING STATS & ABOUT LAYOUT
# ==============================================================================
class TopBanner(SEOMetadataMixin, models.Model):
    heading = models.CharField(max_length=255, blank=True, null=True, verbose_name="Heading")
    sub_heading = models.TextField(blank=True, null=True, verbose_name="Sub Heading")
    image = models.ImageField(
        upload_to=top_banner_image_path,
        blank=True,
        null=True,
        validators=[validate_image_file],
        verbose_name="Banner Image"
    )
    primary_btn_text = models.CharField(
        max_length=100,
        default="Apply For BSc. CSIT",
        blank=True,
        null=True,
        verbose_name="Primary CTA Button Text"
    )
    primary_btn_url = models.CharField(
        max_length=255,
        default="#admissions",
        blank=True,
        null=True,
        verbose_name="Primary CTA Link"
    )
    secondary_btn_text = models.CharField(
        max_length=100,
        default="Explore Syllabus & Modules",
        blank=True,
        null=True,
        verbose_name="Secondary CTA Button Text"
    )
    secondary_btn_url = models.CharField(
        max_length=255,
        default="#program",
        blank=True,
        null=True,
        verbose_name="Secondary CTA Link"
    )
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Top Banner"
        verbose_name_plural = "Top Banners"
        ordering = ['-created_at']
        indexes = [models.Index(fields=['-created_at'])]

    def __str__(self):
        return self.heading or "Top Banner"


class HeroTechnicalTag(models.Model):
    top_banner = models.ForeignKey(
        TopBanner,
        related_name="technical_tags",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Parent Hero Banner"
    )
    icon_class = models.CharField(
        max_length=100,
        default="fa-solid fa-building-columns",
        blank=True,
        null=True,
        verbose_name="FontAwesome / Icon Class"
    )
    title = models.CharField(
        max_length=255,
        default="",
        blank=True,
        null=True,
        verbose_name="Tag Label Text"
    )
    display_order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Hero Technical Tag"
        verbose_name_plural = "Hero Technical Tags"
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return self.title or f"Technical Tag #{self.id}"


class LandingStat(models.Model):
    top_banner = models.ForeignKey(
        TopBanner,
        related_name="landing_stats",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Parent Hero Banner"
    )
    target_number = models.IntegerField(
        default=0,
        blank=True,
        null=True,
        verbose_name="Target Number for Animated Counter"
    )
    prefix = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        default="",
        verbose_name="Value Prefix (e.g. '1st', '$')"
    )
    suffix = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        default="",
        verbose_name="Value Suffix (e.g. '%', '+')"
    )
    label = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default="",
        verbose_name="Primary Metric Label"
    )
    sub_label = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default="",
        verbose_name="Sub Label / Description"
    )
    display_order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Landing Stat / Counter Metric"
        verbose_name_plural = "Landing Stats / Counter Metrics"
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return f"{self.prefix or ''}{self.target_number or ''}{self.suffix or ''} - {self.label or 'Stat'}"


class AboutBannerTitle(SEOMetadataMixin, models.Model):
    badge_text = models.CharField(
        max_length=255,
        default="Brand New Technical Institute",
        blank=True,
        null=True,
        verbose_name="Section Badge Label"
    )
    heading = models.CharField(
        max_length=255,
        default="Setting New Standards for Computer Science Education in Bardibas",
        blank=True,
        null=True,
        verbose_name="Main Headline"
    )
    sub_heading = models.TextField(
        default="Ankur Institute of Engineering and Management Studies (AIEMS) is a newly established technical college dedicated exclusively to computer science and information technology education.",
        blank=True,
        null=True,
        verbose_name="Primary Narrative Paragraph (Paragraph 1)"
    )
    content_paragraph_2 = models.TextField(
        default="In our founding year, we are offering the BSc. CSIT program under university affiliation. Our mission is to train students in fundamental computer science, software development, data structures, and computer networks through intensive lab work.",
        blank=True,
        null=True,
        verbose_name="Secondary Narrative Paragraph (Paragraph 2)"
    )
    image = models.ImageField(
        upload_to=about_banner_image_path,
        blank=True,
        null=True,
        validators=[validate_image_file],
        verbose_name="Featured Section Image"
    )
    floating_badge_icon_class = models.CharField(
        max_length=100,
        default="fa-solid fa-microchip",
        blank=True,
        null=True,
        verbose_name="Floating Badge Icon Class"
    )
    floating_badge_title = models.CharField(
        max_length=255,
        default="Pure Technical Focus",
        blank=True,
        null=True,
        verbose_name="Floating Badge Headline"
    )
    floating_badge_subtitle = models.CharField(
        max_length=255,
        default="Purpose-built for Computer Science",
        blank=True,
        null=True,
        verbose_name="Floating Badge Subtext"
    )
    primary_btn_text = models.CharField(
        max_length=100,
        default="Explore BSc. CSIT Course",
        blank=True,
        null=True,
        verbose_name="Primary CTA Button Text"
    )
    primary_btn_url = models.CharField(
        max_length=255,
        default="#program",
        blank=True,
        null=True,
        verbose_name="Primary CTA Link"
    )
    secondary_btn_text = models.CharField(
        max_length=100,
        default="Contact Admissions Desk",
        blank=True,
        null=True,
        verbose_name="Secondary CTA Link Text"
    )
    secondary_btn_url = models.CharField(
        max_length=255,
        default="#contact",
        blank=True,
        null=True,
        verbose_name="Secondary CTA Link URL"
    )
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "About Banner Title"
        verbose_name_plural = "About Banner Titles"
        ordering = ['-created_at']
        indexes = [models.Index(fields=['-created_at'])]

    def __str__(self):
        return self.heading or "About Banner Title"


class AboutBanner(models.Model):
    about_title = models.ForeignKey(
        AboutBannerTitle,
        related_name="about_banner_items",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="About Banner Title Group"
    )
    icon_class = models.CharField(
        max_length=100,
        default="fa-solid fa-circle-check",
        blank=True,
        null=True,
        verbose_name="FontAwesome / Icon Class"
    )
    heading = models.CharField(max_length=255, blank=True, null=True, verbose_name="Heading")
    content = models.TextField(default='', blank=True, null=True, verbose_name="Content")
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "About Banner Item"
        verbose_name_plural = "About Banner Items"
        ordering = ['-created_at']
        indexes = [models.Index(fields=['-created_at'])]

    def __str__(self):
        return self.heading or "About Banner Item"


class ProgramTitle(SEOMetadataMixin, models.Model):
    heading = models.CharField(max_length=255, blank=True, null=True, verbose_name="Heading")
    sub_heading = models.CharField(max_length=255, blank=True, null=True, verbose_name="Sub Heading")
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Program Section Title"
        verbose_name_plural = "Program Section Titles"
        ordering = ['-created_at']
        indexes = [models.Index(fields=['-created_at'])]

    def __str__(self):
        return self.heading or "Program Section Title"


class Program(models.Model):
    program_title = models.ForeignKey(
        ProgramTitle,
        related_name="program_items",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Program Title Group"
    )
    icon_image = models.ImageField(
        upload_to=program_icon_path,
        blank=True,
        null=True,
        validators=[validate_image_file],
        verbose_name="Icon Image"
    )
    heading = models.CharField(max_length=255, blank=True, null=True, verbose_name="Heading")
    sub_content = models.TextField(blank=True, null=True, verbose_name="Sub Content Summary")
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Academic Program"
        verbose_name_plural = "Academic Programs"
        ordering = ['-created_at']
        indexes = [models.Index(fields=['-created_at'])]

    def __str__(self):
        return self.heading or "Academic Program"

# ==============================================================================
# 2.1 ISOLATED HOMEPAGE PROGRAM SHOWCASE MODELS
# ==============================================================================
class IsolatedHomeShowcaseCard(SEOMetadataMixin, models.Model):
    program_title = models.ForeignKey(
        ProgramTitle,
        related_name="isolated_showcase_cards",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Parent Section Title"
    )
    target_program = models.ForeignKey(
        Program,
        related_name="showcase_target_referrers",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Target Program (Syllabus Link Target)"
    )
    heading = models.CharField(
        max_length=255,
        default="BSc. CSIT",
        verbose_name="Showcase Degree Title"
    )
    sub_content = models.TextField(
        blank=True,
        null=True,
        verbose_name="Main Narrative Copy"
    )
    banner_image = models.ImageField(
        upload_to=top_banner_image_path,
        blank=True,
        null=True,
        validators=[validate_image_file],
        verbose_name="Full-Height Left Banner Image"
    )
    status_badge_text = models.CharField(
        max_length=100,
        default="Now Accepting Applications",
        blank=True,
        null=True,
        verbose_name="Status Badge Text"
    )
    cohort_tag = models.CharField(
        max_length=100,
        default="Inaugural Cohort",
        blank=True,
        null=True,
        verbose_name="Cohort Tag"
    )
    charter_badge_tag = models.CharField(
        max_length=255,
        default="Rajarshi Janak University Affiliated Institution",
        blank=True,
        null=True,
        verbose_name="Affiliation Charter Tag"
    )
    specializations_title = models.CharField(
        max_length=255,
        default="Core Technical Specializations",
        blank=True,
        null=True,
        verbose_name="Specializations Section Headline"
    )
    prerequisite_title = models.CharField(
        max_length=255,
        default="Entry Prerequisites (+2 Science)",
        blank=True,
        null=True,
        verbose_name="Prerequisites Box Title"
    )
    prerequisite_overview = models.TextField(
        blank=True,
        null=True,
        verbose_name="Prerequisites Callout Paragraph"
    )
    apply_button_text = models.CharField(
        max_length=100,
        default="Apply For BSc. CSIT",
        blank=True,
        null=True,
        verbose_name="Apply Button Label"
    )
    eligibility_button_text = models.CharField(
        max_length=100,
        default="Check Your Eligibility",
        blank=True,
        null=True,
        verbose_name="Eligibility Button Label"
    )
    syllabus_button_text = models.CharField(
        max_length=100,
        default="View Full Syllabus",
        blank=True,
        null=True,
        verbose_name="Syllabus Button Label"
    )
    custom_syllabus_redirect_url = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default="",
        verbose_name="Custom Syllabus Link URL (Optional Override)"
    )
    display_order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Homepage Program Showcase Card (Isolated)"
        verbose_name_plural = "Homepage Program Showcase Cards (Isolated)"
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return f"Homepage Showcase Card: {self.heading}"


class IsolatedHomeShowcaseSummaryPoint(models.Model):
    showcase_card = models.ForeignKey(
        IsolatedHomeShowcaseCard,
        related_name="isolated_summary_points",
        on_delete=models.CASCADE,
        verbose_name="Parent Isolated Showcase Card"
    )
    title = models.CharField(max_length=255, verbose_name="Metric Label (e.g. Duration)")
    value = models.CharField(max_length=255, verbose_name="Highlight Value (e.g. 4 Years)")
    sub_text = models.CharField(max_length=255, blank=True, default="", verbose_name="Sub label (e.g. 8 Semesters)")
    icon_class = models.CharField(max_length=100, default="fa-solid fa-clock", verbose_name="FontAwesome Icon Class")
    display_order = models.PositiveIntegerField(default=0, verbose_name="Display Order")

    class Meta:
        verbose_name = "Isolated Showcase Metric Point"
        verbose_name_plural = "Isolated Showcase Metric Points"
        ordering = ['display_order', 'id']

    def __str__(self):
        return f"{self.title}: {self.value}"


class IsolatedHomeShowcaseFeature(models.Model):
    showcase_card = models.ForeignKey(
        IsolatedHomeShowcaseCard,
        related_name="isolated_features",
        on_delete=models.CASCADE,
        verbose_name="Parent Isolated Showcase Card"
    )
    title = models.CharField(max_length=255, verbose_name="Feature Pill Title")
    description = models.TextField(blank=True, default="", verbose_name="Feature Pill Subtext")
    icon_class = models.CharField(max_length=100, default="fa-solid fa-code", verbose_name="FontAwesome Icon Class")
    display_order = models.PositiveIntegerField(default=0, verbose_name="Display Order")

    class Meta:
        verbose_name = "Isolated Showcase Feature Pill"
        verbose_name_plural = "Isolated Showcase Feature Pills"
        ordering = ['display_order', 'id']

    def __str__(self):
        return self.title


class IsolatedHomeShowcaseRequirementRule(models.Model):
    showcase_card = models.ForeignKey(
        IsolatedHomeShowcaseCard,
        related_name="isolated_requirements",
        on_delete=models.CASCADE,
        verbose_name="Parent Isolated Showcase Card"
    )
    content = models.TextField(verbose_name="Prerequisite Rule Sentence")
    display_order = models.PositiveIntegerField(default=0, verbose_name="Display Order")

    class Meta:
        verbose_name = "Isolated Showcase Prerequisite Rule"
        verbose_name_plural = "Isolated Showcase Prerequisite Rules"
        ordering = ['display_order', 'id']

    def __str__(self):
        return self.content[:50]


class CampusTitle(SEOMetadataMixin, models.Model):
    heading = models.CharField(max_length=255, blank=True, null=True, verbose_name="Heading")
    sub_heading = models.CharField(max_length=255, blank=True, null=True, verbose_name="Sub Heading")
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Campus Section Title"
        verbose_name_plural = "Campus Section Titles"
        ordering = ['-created_at']
        indexes = [models.Index(fields=['-created_at'])]

    def __str__(self):
        return self.heading or "Campus Section Title"


class CampusFacility(models.Model):
    campus_title = models.ForeignKey(
        CampusTitle,
        related_name="campus_items",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Campus Title Group"
    )
    image = models.ImageField(
        upload_to=campus_facility_path,
        blank=True,
        null=True,
        validators=[validate_image_file],
        verbose_name="Facility Image"
    )
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Campus Facility"
        verbose_name_plural = "Campus Facilities"
        ordering = ['-created_at']
        indexes = [models.Index(fields=['-created_at'])]

    def __str__(self):
        return str(self.campus_title) if self.campus_title else "Campus Facility"


class NewsTitle(SEOMetadataMixin, models.Model):
    heading = models.CharField(max_length=255, blank=True, null=True, verbose_name="Heading")
    sub_heading = models.CharField(max_length=255, blank=True, null=True, verbose_name="Sub Heading")
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "News Section Title"
        verbose_name_plural = "News Section Titles"
        ordering = ['-created_at']
        indexes = [models.Index(fields=['-created_at'])]

    def __str__(self):
        return self.heading or "News Section Title"


class NewsEvent(models.Model):
    news_title = models.ForeignKey(
        NewsTitle,
        related_name="news_items",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="News Title Group"
    )
    date = models.DateField(blank=True, null=True, verbose_name="Event Date")
    heading = models.CharField(max_length=255, blank=True, null=True, verbose_name="Heading")
    content = models.TextField(default='', blank=True, null=True, verbose_name="Content")
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "News Event"
        verbose_name_plural = "News Events"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['date'])
        ]

    def __str__(self):
        return self.heading or "News Event"

# ==============================================================================
# 3. ADMISSIONS & INQUIRY CONFIGURATION
# ==============================================================================
class AdmissionContactDetail(models.Model):
    heading = models.CharField(max_length=255, blank=True, null=True, verbose_name="Heading")
    sub_heading = models.CharField(max_length=255, blank=True, null=True, verbose_name="Sub Heading")
    mail_id = models.CharField(max_length=255, blank=True, null=True, validators=[EmailValidator()], verbose_name="Email Address")
    contact = models.CharField(max_length=20, blank=True, null=True, validators=[phone_validator], verbose_name="Contact Number")
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Admission Contact Detail"
        verbose_name_plural = "Admission Contact Details"
        ordering = ['-created_at']
        indexes = [models.Index(fields=['-created_at'])]

    def __str__(self):
        return self.heading or "Admission Contact Detail"


class AdmissionDetailTitle(models.Model):
    heading = models.CharField(max_length=255, blank=True, null=True, verbose_name="Heading")
    sub_heading = models.CharField(max_length=255, blank=True, null=True, verbose_name="Sub Heading")
    sub_content = models.CharField(max_length=255, blank=True, null=True, verbose_name="Sub Content Label")
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Admission Detail Section Title"
        verbose_name_plural = "Admission Detail Section Titles"
        ordering = ['-created_at']
        indexes = [models.Index(fields=['-created_at'])]

    def __str__(self):
        return self.heading or "Admission Detail Section Title"


class AdmissionCriteria(models.Model):
    admission_detail = models.ForeignKey(
        AdmissionDetailTitle,
        related_name="criteria_items",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Admission Detail Title Parent"
    )
    content = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Criteria Rule Description"
    )
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Admission Criteria Rule"
        verbose_name_plural = "Admission Criteria Rules"
        ordering = ['-created_at']
        indexes = [models.Index(fields=['-created_at'])]

    def __str__(self):
        return self.content or "Admission Criteria Rule"

# ==============================================================================
# 4. FACULTY & TEAMS DIRECTORY
# ==============================================================================
class TeamTitle(SEOMetadataMixin, models.Model):
    heading = models.CharField(max_length=255, blank=True, null=True, verbose_name="Heading")
    sub_heading = models.CharField(max_length=255, blank=True, null=True, verbose_name="Sub Heading")
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Team Section Title"
        verbose_name_plural = "Team Section Titles"
        ordering = ['-created_at']
        indexes = [models.Index(fields=['-created_at'])]

    def __str__(self):
        return self.heading or "Team Section Title"


class TeamFaculty(models.Model):
    team_title = models.ForeignKey(
        TeamTitle,
        related_name="faculty_items",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Team Title Group"
    )
    heading = models.CharField(max_length=255, blank=True, null=True, verbose_name="Heading")
    sub_heading = models.CharField(max_length=255, blank=True, null=True, verbose_name="Sub Heading")
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Team Department/Faculty Group"
        verbose_name_plural = "Team Department/Faculty Groups"
        ordering = ['-created_at']
        indexes = [models.Index(fields=['-created_at'])]

    def __str__(self):
        return self.heading or "Team Faculty Group"


class TeamMember(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Full Name")
    profile_image = models.ImageField(
        upload_to=team_member_path,
        blank=True,
        null=True,
        validators=[validate_image_file],
        verbose_name="Profile Portrait"
    )
    faculty = models.ForeignKey(
        TeamFaculty,
        related_name="member_items",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Department Faculty Assignment"
    )
    designation = models.CharField(max_length=255, blank=True, null=True, verbose_name="Designation Title")
    message = models.TextField(default='', blank=True, null=True, verbose_name="Leadership Message Statement")
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Team Member Profile"
        verbose_name_plural = "Team Member Profiles"
        ordering = ['-created_at']
        indexes = [models.Index(fields=['-created_at'])]

    def __str__(self):
        return self.name or "Team Member"

# ==============================================================================
# 5. SUBMISSIONS & APPLICATION LOGS
# ==============================================================================
class ApplyJobDetail(models.Model):
    heading = models.CharField(max_length=255, blank=True, null=True, verbose_name="Heading")
    sub_heading = models.CharField(max_length=255, blank=True, null=True, verbose_name="Sub Heading")
    mail_id = models.CharField(max_length=255, blank=True, null=True, validators=[EmailValidator()], verbose_name="HR Email")
    contact = models.CharField(max_length=20, blank=True, null=True, validators=[phone_validator], verbose_name="HR Contact Number")
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Careers Section Information"
        verbose_name_plural = "Careers Section Information"
        ordering = ['-created_at']
        indexes = [models.Index(fields=['-created_at'])]

    def __str__(self):
        return self.heading or "Careers Section Information"


class ContactUs(models.Model):
    name = models.CharField(max_length=255, verbose_name="Inquirer Name")
    email = models.CharField(max_length=255, validators=[EmailValidator()], verbose_name="Email ID")
    contact = models.CharField(
        max_length=20,
        validators=[phone_validator],
        verbose_name="Contact Number"
    )
    city = models.CharField(max_length=255, verbose_name="City Address")
    message = models.TextField(max_length=1000, verbose_name="Inquiry Description Text")
    created_at = models.DateTimeField(default=now, verbose_name="Submitted Timestamp")

    class Meta:
        verbose_name = "Contact Message Log"
        verbose_name_plural = "Contact Message Logs"
        ordering = ['-created_at']
        indexes = [models.Index(fields=['-created_at'])]

    def __str__(self):
        return f"{self.name} - {self.email}"


class ApplyCourse(models.Model):
    name = models.CharField(max_length=255, verbose_name="Applicant Name")
    gender = models.CharField(
        max_length=255,
        choices=choices.GenderChoices.choices,
        default="",
        verbose_name="Gender Identity"
    )
    contact = models.CharField(max_length=20, validators=[phone_validator], verbose_name="Contact Number")
    email = models.CharField(max_length=255, validators=[EmailValidator()], verbose_name="Email Address")
    program = models.ForeignKey(
        Program,
        related_name="apply_course_program",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Applied Program Course"
    )
    institution = models.CharField(max_length=255, verbose_name="Previous High School / 12th Institution")
    message = models.TextField(max_length=1000, blank=True, default="", verbose_name="Additional Notes")
    created_at = models.DateTimeField(default=now, verbose_name="Applied At")

    class Meta:
        verbose_name = "Program Course Admission Application"
        verbose_name_plural = "Program Course Admission Applications"
        ordering = ['-created_at']
        indexes = [models.Index(fields=['-created_at'])]

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Vacancy Job Position Name")
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Career Vacancy Job Position"
        verbose_name_plural = "Career Vacancy Job Positions"
        ordering = ['name']

    def __str__(self):
        return self.name


class ApplyPosition(models.Model):
    name = models.CharField(max_length=255, verbose_name="Job Candidate Name")
    gender = models.CharField(
        max_length=255,
        choices=choices.GenderChoices.choices,
        default="",
        verbose_name="Gender Identity"
    )
    contact = models.CharField(max_length=20, validators=[phone_validator], verbose_name="Contact Number")
    email = models.CharField(max_length=255, validators=[EmailValidator()], verbose_name="Email Address")
    position = models.ForeignKey(
        Position,
        related_name="apply_position",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Applied Vacancy Position"
    )
    document = models.FileField(
        upload_to=apply_position_resume_path,
        blank=True,
        null=True,
        validators=[validate_document_file],
        verbose_name="CV / Resume PDF Document"
    )
    message = models.TextField(max_length=1000, blank=True, default="", verbose_name="Cover Message")
    created_at = models.DateTimeField(default=now, verbose_name="Applied At")

    class Meta:
        verbose_name = "Career Job Application Form Submission"
        verbose_name_plural = "Career Job Application Form Submissions"
        ordering = ['-created_at']
        indexes = [models.Index(fields=['-created_at'])]

    def __str__(self):
        return self.name

# ==============================================================================
# 6. FORM LANDING BANNERS
# ==============================================================================
class ApplyForCourseBanner(SEOMetadataMixin, models.Model):
    heading = models.CharField(max_length=255, blank=True, null=True, verbose_name="Heading")
    sub_heading = models.CharField(max_length=255, blank=True, null=True, verbose_name="Sub Heading")
    image = models.ImageField(
        upload_to=top_banner_image_path,
        blank=True,
        null=True,
        validators=[validate_image_file],
        verbose_name="Banner Image"
    )
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Application Course Landing Banner"
        verbose_name_plural = "Application Course Landing Banners"
        ordering = ['-created_at']
        indexes = [models.Index(fields=['-created_at'])]

    def __str__(self):
        return self.heading or "Application Course Landing Banner"


class ApplyForPositionBanner(SEOMetadataMixin, models.Model):
    heading = models.CharField(max_length=255, blank=True, null=True, verbose_name="Heading")
    sub_heading = models.CharField(max_length=255, blank=True, null=True, verbose_name="Sub Heading")
    image = models.ImageField(
        upload_to=top_banner_image_path,
        blank=True,
        null=True,
        validators=[validate_image_file],
        verbose_name="Banner Image"
    )
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Application Position Landing Banner"
        verbose_name_plural = "Application Position Landing Banners"
        ordering = ['-created_at']
        indexes = [models.Index(fields=['-created_at'])]

    def __str__(self):
        return self.heading or "Application Position Landing Banner"

# ==============================================================================
# 7. GLOBAL FOOTER CONFIGURATION
# ==============================================================================
class FooterConfig(models.Model):
    logo = models.ImageField(
        upload_to=footer_logo_path,
        validators=[validate_image_file],
        blank=True,
        null=True,
        verbose_name="Footer Logo"
    )
    branding_description = models.TextField(
        blank=True,
        null=True,
        default="",
        verbose_name="Branding Description"
    )
    facebook_url = models.URLField(blank=True, null=True, verbose_name="Facebook URL")
    linkedin_url = models.URLField(blank=True, null=True, verbose_name="LinkedIn URL")
    instagram_url = models.URLField(blank=True, null=True, verbose_name="Instagram URL")
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Footer Configuration"
        verbose_name_plural = "Footer Configurations"
        ordering = ['-created_at']
        indexes = [models.Index(fields=['-created_at'])]

    def __str__(self):
        return "Footer Configuration Settings"


class FooterLink(models.Model):
    LINK_CATEGORY_CHOICES = (
        ('navigation', 'Navigation Column'),
        ('academics', 'Academics Column'),
    )

    footer_config = models.ForeignKey(
        FooterConfig,
        related_name="footer_links",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Footer Configuration Parent"
    )
    category = models.CharField(
        max_length=50,
        choices=LINK_CATEGORY_CHOICES,
        default='navigation',
        blank=True,
        null=True,
        verbose_name="Footer Section / Column"
    )
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name="Link Label")
    url = models.CharField(max_length=500, blank=True, null=True, verbose_name="URL / Path")
    display_order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    open_in_new_tab = models.BooleanField(default=False, verbose_name="Open In New Tab")
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Footer Link"
        verbose_name_plural = "Footer Links"
        ordering = ['category', 'display_order', '-created_at']
        indexes = [
            models.Index(fields=['display_order']),
            models.Index(fields=['is_active']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return f"[{self.get_category_display() if self.category else 'Link'}] {self.title or ''} ({self.url or ''})"

# ==============================================================================
# 8. CMS FAQS & DYNAMIC PAGE CONTENT
# ==============================================================================
class FAQCategory(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Category Name")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Slug")
    display_order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "FAQ Category"
        verbose_name_plural = "FAQ Categories"
        ordering = ['display_order', '-created_at']
        indexes = [
            models.Index(fields=['display_order']),
            models.Index(fields=['slug'])
        ]

    def __str__(self):
        return self.name or "FAQ Category"


class FAQItem(models.Model):
    category = models.ForeignKey(
        FAQCategory,
        related_name="faq_items",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Category Parent"
    )
    question = models.CharField(max_length=255, blank=True, null=True, verbose_name="Question")
    answer = models.TextField(blank=True, null=True, verbose_name="Answer")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    display_order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "FAQ Item"
        verbose_name_plural = "FAQ Items"
        ordering = ['display_order', '-created_at']
        indexes = [
            models.Index(fields=['display_order']),
            models.Index(fields=['is_active'])
        ]

    def __str__(self):
        return self.question or "FAQ Item"


class DynamicPageContent(SEOMetadataMixin, models.Model):
    page_key = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Page Key"
    )
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name="Page Title")
    subtitle = models.CharField(max_length=255, blank=True, null=True, verbose_name="Page Subtitle")
    content_json = models.JSONField(
        blank=True,
        null=True,
        verbose_name="Structured Content (JSON)"
    )
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    created_at = models.DateTimeField(default=now, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Dynamic Page Content"
        verbose_name_plural = "Dynamic Page Contents"
        ordering = ['page_key']
        indexes = [
            models.Index(fields=['page_key']),
            models.Index(fields=['is_active'])
        ]

    def __str__(self):
        return f"{self.title or 'Page'} ({self.page_key})"

# ==============================================================================
# 9. DYNAMIC CMS-DRIVEN EMAIL NOTIFICATION CONFIGURATION MODEL
# ==============================================================================
class NotificationSetting(models.Model):
    class ProviderChoices(models.TextChoices):
        CUSTOM_SMTP = "smtp", "Custom SMTP"
        GMAIL_SMTP = "gmail", "Gmail SMTP"
        OUTLOOK_SMTP = "outlook", "Outlook / Office 365"

    class EncryptionChoices(models.TextChoices):
        STARTTLS = "tls", "STARTTLS (Explicit TLS)"
        SSL = "ssl", "SSL/TLS"
        NONE = "none", "None (Plain)"

    # Profile Settings
    name = models.CharField(
        max_length=255,
        default="Global Notification Configuration",
        verbose_name="Configuration Profile Name"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Is Active Globally?",
        help_text="Enable/disable email notification dispatches across all forms on the site."
    )

    # Dedicated Email Branding & Logo
    email_logo = models.ImageField(
        upload_to=email_logo_path,
        blank=True,
        null=True,
        validators=[validate_email_image_file],
        verbose_name="Email Template Header Logo",
        help_text="Dedicated raster (JPG/JPEG/PNG/WEBP) logo used at the top of outgoing emails. Recommended size: PNG up to 300px wide. SVG is not allowed because email clients cannot render it inline reliably."
    )
    email_header_bg_color = models.CharField(
        max_length=50,
        default="#0e0e54",
        blank=True,
        null=True,
        verbose_name="Email Header Accent Color (Hex)",
        help_text="Primary background color for the email banner header (e.g., #0e0e54 or #009444)."
    )
    email_footer_text = models.CharField(
        max_length=255,
        default="Ankur Institute of Engineering and Management Studies (AIEMS)",
        blank=True,
        null=True,
        verbose_name="Email Footer Institution Name"
    )
    email_footer_address = models.CharField(
        max_length=255,
        default="Bardibas, Mahottari, Nepal",
        blank=True,
        null=True,
        verbose_name="Email Footer Physical Address"
    )

    # Provider & Network Settings
    provider = models.CharField(
        max_length=50,
        choices=ProviderChoices.choices,
        default=ProviderChoices.CUSTOM_SMTP,
        verbose_name="Email Provider Scheme"
    )
    smtp_host = models.CharField(
        max_length=255,
        default="smtp.gmail.com",
        verbose_name="SMTP Server Host"
    )
    smtp_port = models.PositiveIntegerField(
        default=587,
        verbose_name="SMTP Network Port"
    )
    encryption = models.CharField(
        max_length=20,
        choices=EncryptionChoices.choices,
        default=EncryptionChoices.STARTTLS,
        verbose_name="Encryption Protocol"
    )

    # Credentials
    smtp_username = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="SMTP Handshake Username / Email"
    )
    smtp_password = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="SMTP Password / App Credential"
    )

    # Sender Identity
    default_from_email = models.EmailField(
        default="info@aiems.edu.np",
        verbose_name="Default From Email Envelope Address"
    )
    default_sender_name = models.CharField(
        max_length=255,
        default="AIEMS Admissions & HR Desk",
        verbose_name="Default Sender Display Name"
    )

    # Admin Recipient Emails
    primary_admin_email = models.EmailField(
        default="admissions@aiems.edu.np",
        verbose_name="Primary Admin Notification Email",
        help_text="Dedicated primary college email address to receive submission notifications."
    )
    secondary_admin_email = models.EmailField(
        blank=True,
        default="",
        verbose_name="Secondary Admin Notification Email (Optional)",
        help_text="Optional secondary college email address for CC/alert notifications."
    )

    # Notification Toggles
    send_applicant_confirmation = models.BooleanField(
        default=True,
        verbose_name="Send Confirmation Email to Applicants?"
    )
    send_admin_notification = models.BooleanField(
        default=True,
        verbose_name="Send Alert Email to College Admin Team?"
    )

    # Customizable Message Templates & Callouts
    next_steps_heading = models.CharField(
        max_length=255,
        default="What Happens Next?",
        blank=True,
        null=True,
        verbose_name="Course Confirmation 'Next Steps' Box Title"
    )
    next_steps_body = models.TextField(
        default="Our counseling team will verify your academic background and reach out with details regarding entrance schedules and fee structures.",
        blank=True,
        null=True,
        verbose_name="Course Confirmation 'Next Steps' Box Content"
    )

    course_app_subject = models.CharField(
        max_length=255,
        default="Application Received: {program} at AIEMS",
        verbose_name="Course Application Subject Template"
    )
    course_app_applicant_body = models.TextField(
        default="Thank you for applying to AIEMS. We have received your application details for the program. Our admissions counseling desk will review your submission and contact you shortly.",
        verbose_name="Course Application Applicant Message Body"
    )

    job_app_subject = models.CharField(
        max_length=255,
        default="Application Received for {position} - AIEMS",
        verbose_name="Job Application Subject Template"
    )
    job_app_applicant_body = models.TextField(
        default="Thank you for submitting your career application. Your resume and credentials have been delivered to our HR department for evaluation.",
        verbose_name="Job Application Applicant Message Body"
    )

    contact_subject = models.CharField(
        max_length=255,
        default="Inquiry Received - AIEMS Bardibas",
        verbose_name="Contact Inquiry Subject Template"
    )
    contact_applicant_body = models.TextField(
        default="Thank you for reaching out to AIEMS. We have received your inquiry message and our administration team will contact you soon.",
        verbose_name="Contact Inquiry Applicant Message Body"
    )

    # Timeout & Reliability
    timeout = models.PositiveIntegerField(
        default=15,
        verbose_name="Connection Timeout Threshold (Seconds)"
    )
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Notification Setting"
        verbose_name_plural = "Notification Settings"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({'Active' if self.is_active else 'Disabled'})"

    def get_admin_email_list(self):
        emails = []
        if self.primary_admin_email and self.primary_admin_email.strip():
            emails.append(self.primary_admin_email.strip())
        if self.secondary_admin_email and self.secondary_admin_email.strip():
            emails.append(self.secondary_admin_email.strip())
        return emails