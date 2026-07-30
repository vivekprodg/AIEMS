from django.db import models

class GenderChoices(models.TextChoices):
    MALE = "male", "Male"
    FEMALE = "female", "Female"
    OTHER = "other", "Other"

class CourseDetail(models.TextChoices):
    NAME = "course name", "Course Name"
    CODE = "course code", "Course Code"
    DURATION = "course duration", "Course Duration"
    HOURS = "credit hours", "Credit Hours"
    REQUIREMENT = "entry requirement", "Entry Requirement"
    INTAKE = "intake", "Intake"
    TIME = "time", "Time"
    ACCREDITATION = "accreditation", "Accreditation"