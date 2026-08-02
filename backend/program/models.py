from django.db import models
from django.utils.timezone import now

from home.models import Program, validate_image_file, secure_file_rename
from home import choices


def program_asset_path(instance, filename):
    return secure_file_rename(instance, filename, 'programs')


class ProgramBannerImage(models.Model):
    program = models.ForeignKey(
        Program,
        related_name="program_banner",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Associated Program"
    )
    image = models.ImageField(
        upload_to=program_asset_path,
        validators=[validate_image_file],
        blank=True,
        null=True,
        verbose_name="Hero Banner Media Asset"
    )
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Program Banner Image"
        verbose_name_plural = "Program Banner Images"
        ordering = ['-created_at']

    def __str__(self):
        return f"Banner - {self.program.heading if self.program else 'Unassigned'}"


class ProgramSummaryPoints(models.Model):
    program = models.ForeignKey(
        Program,
        related_name="program_summary",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Associated Program"
    )
    icon_image = models.ImageField(
        upload_to=program_asset_path,
        validators=[validate_image_file],
        blank=True,
        null=True,
        verbose_name="Custom Icon Image"
    )
    icon_class = models.CharField(
        max_length=100,
        default="fa-solid fa-clock",
        verbose_name="FontAwesome Icon Class"
    )
    title = models.CharField(
        max_length=255,
        choices=choices.CourseDetail.choices,
        default="",
        verbose_name="Metric Label / Category"
    )
    value = models.CharField(max_length=255, verbose_name="Metric Highlight Value (e.g. '4 Years')")
    sub_text = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Sub label (e.g. '8 Semesters')"
    )
    display_order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Program Metric Highlight"
        verbose_name_plural = "Program Metric Highlights"
        ordering = ['display_order', 'id']

    def __str__(self):
        return f"{self.title}: {self.value}"


class AboutProgram(models.Model):
    program = models.ForeignKey(
        Program,
        related_name="about_programs",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Associated Program"
    )
    small_title = models.CharField(
        max_length=255,
        default="",
        blank=True,
        verbose_name="Small Section Tag Label"
    )
    title = models.CharField(
        max_length=255,
        default="",
        verbose_name="Main Headline"
    )
    image = models.ImageField(
        upload_to=program_asset_path,
        validators=[validate_image_file],
        blank=True,
        null=True,
        verbose_name="Overview Feature Photo"
    )
    content = models.TextField(default="", verbose_name="Primary Narrative Paragraph")
    content_paragraph_2 = models.TextField(default="", blank=True, verbose_name="Secondary Narrative Paragraph")

    charter_badge_tag = models.CharField(
        max_length=100,
        default="",
        blank=True,
        verbose_name="Charter Badge Tag Label"
    )
    charter_badge_title = models.CharField(
        max_length=255,
        default="",
        blank=True,
        verbose_name="Charter Badge Headline"
    )
    charter_badge_subtext = models.CharField(
        max_length=255,
        default="",
        blank=True,
        verbose_name="Charter Badge Subtext"
    )

    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Program Narrative & Overview"
        verbose_name_plural = "Program Narratives & Overviews"
        ordering = ['-created_at']

    def __str__(self):
        return self.title or f"About {self.program.heading if self.program else 'Program'}"


class AboutProgramFeature(models.Model):
    about_program = models.ForeignKey(
        AboutProgram,
        related_name="features",
        on_delete=models.CASCADE,
        verbose_name="Parent Narrative Record"
    )
    title = models.CharField(max_length=255, verbose_name="Feature Headline")
    description = models.TextField(verbose_name="Feature Description")
    icon_class = models.CharField(
        max_length=100,
        default="fa-solid fa-code",
        verbose_name="FontAwesome Icon Class"
    )
    display_order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Program Feature Highlight"
        verbose_name_plural = "Program Feature Highlights"
        ordering = ['display_order', 'id']

    def __str__(self):
        return self.title


class ProgramEntryRequirement(models.Model):
    program = models.ForeignKey(
        Program,
        related_name="entry_requirements",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Associated Program"
    )
    title = models.CharField(
        max_length=255,
        default="",
        verbose_name="Section Title Label"
    )
    icon = models.ImageField(
        upload_to=program_asset_path,
        validators=[validate_image_file],
        blank=True,
        null=True,
        verbose_name="Custom Section Icon Asset"
    )
    icon_class = models.CharField(
        max_length=100,
        default="fa-solid fa-user-graduate",
        verbose_name="FontAwesome Icon Class"
    )
    content = models.TextField(default="", verbose_name="General Prerequisite Overview Copy")
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Entrance Eligibility Section"
        verbose_name_plural = "Entrance Eligibility Sections"
        ordering = ['-created_at']

    def __str__(self):
        return self.title or f"Eligibility - {self.program.heading if self.program else 'Unassigned'}"


class ProgramEntryRequirementItem(models.Model):
    entry_requirement = models.ForeignKey(
        ProgramEntryRequirement,
        related_name="items",
        on_delete=models.CASCADE,
        verbose_name="Parent Requirement Group"
    )
    content = models.TextField(verbose_name="Checklist Requirement Rule")
    display_order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Eligibility Checklist Item"
        verbose_name_plural = "Eligibility Checklist Items"
        ordering = ['display_order', 'id']

    def __str__(self):
        return self.content[:50]


class CourseDetail(models.Model):
    program = models.ForeignKey(
        Program,
        related_name="course_details",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Associated Program"
    )
    semester = models.CharField(max_length=100, verbose_name="Semester Identifier (e.g. '1', '5')")
    title = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Semester Title (e.g. 'Semester I — Foundation')"
    )
    credit_summary_text = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Credit Summary Badge (e.g. '15 Credit Hours')"
    )
    has_electives = models.BooleanField(
        default=False,
        verbose_name="Contains Elective Selection Stream?"
    )
    elective_stream_title = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Elective Section Title"
    )
    display_order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Semester Curriculum Group"
        verbose_name_plural = "Semester Curriculum Groups"
        ordering = ['display_order', 'id']

    def __str__(self):
        return f"{self.program.heading if self.program else 'Program'} - Semester {self.semester}"


class CourseDetailChild(models.Model):
    course_detail = models.ForeignKey(
        CourseDetail,
        related_name="courses",
        on_delete=models.CASCADE,
        verbose_name="Parent Semester Group"
    )
    course_name = models.CharField(max_length=255, verbose_name="Course Name")
    course_code = models.CharField(max_length=50, verbose_name="Course Code (e.g. CSC109)")
    credit_hours = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Credit Hours (Optional)"
    )
    course_type = models.CharField(
        max_length=100,
        blank=True,
        default="Core Theory + Lab",
        verbose_name="Course Type Badge"
    )
    is_elective = models.BooleanField(default=False, verbose_name="Is Elective Subject?")
    description = models.TextField(
        blank=True,
        default="",
        verbose_name="Elective Subject Description"
    )
    display_order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Curriculum Subject Item"
        verbose_name_plural = "Curriculum Subject Items"
        ordering = ['display_order', 'id']

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"


class CourseDetailChildElectiveOption(models.Model):
    course_detail_child = models.ForeignKey(
        CourseDetailChild,
        related_name="elective_options",
        on_delete=models.CASCADE,
        verbose_name="Parent Elective Subject"
    )
    course_name = models.CharField(max_length=255, verbose_name="Elective Course Name")
    course_code = models.CharField(max_length=50, verbose_name="Elective Course Code (e.g. SCIT 421)")
    credit_hours = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Credit Hours (Optional)"
    )
    description = models.TextField(blank=True, default="", verbose_name="Elective Course Description")
    display_order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Elective Course Option"
        verbose_name_plural = "Elective Course Options"
        ordering = ['display_order', 'id']

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"


class ProgramIndustryCertification(models.Model):
    program = models.ForeignKey(
        Program,
        related_name="industry_certifications",
        on_delete=models.CASCADE,
        verbose_name="Associated Program"
    )
    partner_name = models.CharField(max_length=255, verbose_name="Partner / Vendor Name")
    category_badge = models.CharField(max_length=100, verbose_name="Category Badge")
    badge_color_class = models.CharField(
        max_length=100,
        default="text-primary bg-primary/10",
        verbose_name="Tailwind Badge Style Class"
    )
    description = models.TextField(verbose_name="Certification Description")
    track_label = models.CharField(max_length=100, verbose_name="Track Tag")
    icon_class = models.CharField(
        max_length=100,
        default="fa-solid fa-certificate",
        verbose_name="FontAwesome Icon Class"
    )
    display_order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Industry Certification Co-Track"
        verbose_name_plural = "Industry Certification Co-Tracks"
        ordering = ['display_order', 'id']

    def __str__(self):
        return f"{self.partner_name} - {self.track_label}"


class CareerOutcomes(models.Model):
    program = models.ForeignKey(
        Program,
        related_name="career_outcomes",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Associated Program"
    )
    title = models.CharField(max_length=255, default="", verbose_name="Section Title")
    content = models.TextField(default="", blank=True, verbose_name="Section Intro Copy")
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Career Outlook Group"
        verbose_name_plural = "Career Outlook Groups"
        ordering = ['-created_at']

    def __str__(self):
        return self.title or f"Careers - {self.program.heading if self.program else 'Program'}"


class CareerOutcomeChild(models.Model):
    career_outcome = models.ForeignKey(
        CareerOutcomes,
        related_name="child_outcomes",
        on_delete=models.CASCADE,
        verbose_name="Parent Career Group"
    )
    icon_image = models.ImageField(
        upload_to=program_asset_path,
        validators=[validate_image_file],
        blank=True,
        null=True,
        verbose_name="Custom Icon Image"
    )
    icon_class = models.CharField(
        max_length=100,
        default="fa-solid fa-code",
        verbose_name="FontAwesome Icon Class"
    )
    title = models.CharField(max_length=255, verbose_name="Job Role Title")
    sub_title = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="Role Specialization / Scope"
    )
    display_order = models.PositiveIntegerField(default=0, verbose_name="Display Order")
    created_at = models.DateTimeField(default=now, verbose_name="Created At")

    class Meta:
        verbose_name = "Graduate Career Role"
        verbose_name_plural = "Graduate Career Roles"
        ordering = ['display_order', 'id']

    def __str__(self):
        return self.title