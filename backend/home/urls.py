from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    # Global Settings, Navbar & Ticker ViewSets
    SiteGlobalSettingsViewSet,
    NavbarLinkViewSet,
    AnnouncementTickerItemViewSet,
    EligibilityCalculatorConfigViewSet,

    # Core CMS Content Block ViewSets
    TopBannerViewSet,
    AboutBannerTitleViewSet,
    AboutBannerViewSet,
    ProgramTitleViewSet,
    ProgramViewSet,
    CampusTitleViewSet,
    CampusFacilityViewSet,
    NewsTitleViewSet,
    NewsItemViewSet,

    # Admissions Section ViewSets
    AdmissionContactDetailViewSet,
    AdmissionDetailTitleViewSet,
    AdmissionCriteriaViewSet,

    # Team & Faculty Section ViewSets
    TeamTitleViewSet,
    TeamFacultyViewSet,
    TeamMemberViewSet,

    # Public Forms, Careers & Contact ViewSets
    ContactUsViewSet,
    ApplyCourseViewSet,
    ApplyPositionViewSet,
    ApplyJobDetailViewSet,

    # Static Page / Forms Landing Banners
    ApplyForCourseBannerViewSet,
    ApplyForPositionBannerViewSet,

    # Global System Settings & Configurations ViewSets
    FooterConfigViewSet,
    FooterLinkViewSet,

    # Integrated CMS Content ViewSets
    FAQCategoryViewSet,
    FAQItemViewSet,
    DynamicPageContentViewSet,

    # Unified Dynamic Layout View
    ListHomeView
)

router = DefaultRouter()

# ==============================================================================
# 1. SITE CONFIGURATION, NAVBAR & ANNOUNCEMENTS
# ==============================================================================
router.register(r'site-settings', SiteGlobalSettingsViewSet, basename='site-settings')
router.register(r'navbar-links', NavbarLinkViewSet, basename='navbar-links')
router.register(r'announcements', AnnouncementTickerItemViewSet, basename='announcements')
router.register(r'eligibility-config', EligibilityCalculatorConfigViewSet, basename='eligibility-config')

# ==============================================================================
# 2. CORE CMS & CONTENT MANAGEMENT ENDPOINTS
# ==============================================================================
router.register(r'topbanners', TopBannerViewSet, basename='topbanners')
router.register(r'aboutbannertitles', AboutBannerTitleViewSet, basename='aboutbannertitles')
router.register(r'aboutbanners', AboutBannerViewSet, basename='aboutbanners')
router.register(r'programtitles', ProgramTitleViewSet, basename='programtitles')
router.register(r'programs', ProgramViewSet, basename='programs')
router.register(r'campustitles', CampusTitleViewSet, basename='campustitles')
router.register(r'campusfacilities', CampusFacilityViewSet, basename='campusfacilities')
router.register(r'newstitles', NewsTitleViewSet, basename='newstitles')
router.register(r'newsitems', NewsItemViewSet, basename='newsitems')

# ==============================================================================
# 3. ADMISSIONS & COURSE ENROLLMENT DETAILS
# ==============================================================================
router.register(r'admissioncontactdetails', AdmissionContactDetailViewSet, basename='admissioncontactdetails')
router.register(r'admissiondetailtitles', AdmissionDetailTitleViewSet, basename='admissiondetailtitles')
router.register(r'admissioncriteria', AdmissionCriteriaViewSet, basename='admissioncriteria')

# ==============================================================================
# 4. FACULTY, MANAGEMENT & ORGANIZATIONAL TEAMS
# ==============================================================================
router.register(r'teamtitles', TeamTitleViewSet, basename='teamtitles')
router.register(r'teamfaculties', TeamFacultyViewSet, basename='teamfaculties')
router.register(r'teammembers', TeamMemberViewSet, basename='teammembers')

# ==============================================================================
# 5. PUBLIC ENGAGEMENT, INQUIRIES & ADMISSION FORM SUBMISSIONS
# ==============================================================================
router.register(r'contact-us', ContactUsViewSet, basename='contactus')
router.register(r'apply-course', ApplyCourseViewSet, basename='applycourse')
router.register(r'apply-position', ApplyPositionViewSet, basename='applyposition')
router.register(r'applyjobdetails', ApplyJobDetailViewSet, basename='applyjobdetails')

# ==============================================================================
# 6. LANDING PAGE CONTENT BANNERS
# ==============================================================================
router.register(r'apply-course-banner', ApplyForCourseBannerViewSet, basename='apply-course-banner')
router.register(r'apply-position-banner', ApplyForPositionBannerViewSet, basename='apply-position-banner')

# ==============================================================================
# 7. GLOBAL FOOTER CONFIGURATION
# ==============================================================================
router.register(r'footer-config', FooterConfigViewSet, basename='footer-config')
router.register(r'footer-links', FooterLinkViewSet, basename='footer-links')

# ==============================================================================
# 8. CMS FAQS & DYNAMIC PAGE CONTENT
# ==============================================================================
router.register(r'faq-categories', FAQCategoryViewSet, basename='faq-categories')
router.register(r'faq-items', FAQItemViewSet, basename='faq-items')
router.register(r'page-contents', DynamicPageContentViewSet, basename='page-contents')

# ==============================================================================
# URLPATTERNS DEFINITION
# ==============================================================================
urlpatterns = [
    path('', include(router.urls)),
    path('home-content/', ListHomeView.as_view(), name='home-content'),
]