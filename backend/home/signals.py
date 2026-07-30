import logging
import threading
import urllib.parse
import urllib.request
import json
from django.db.models.signals import post_save, post_delete
from django.core.cache import cache
from decouple import config

from home.models import (
    SiteGlobalSettings, NavbarLink, AnnouncementTickerItem, EligibilityCalculatorConfig,
    EligibilityStreamOption, TopBanner as HomeTopBanner, HeroTechnicalTag, LandingStat,
    AboutBannerTitle, AboutBanner, ProgramTitle, Program,
    IsolatedHomeShowcaseCard, IsolatedHomeShowcaseSummaryPoint, IsolatedHomeShowcaseFeature, IsolatedHomeShowcaseRequirementRule,
    CampusTitle as HomeCampusTitle, CampusFacility, NewsTitle, NewsEvent, AdmissionContactDetail,
    AdmissionDetailTitle, AdmissionCriteria, TeamTitle, TeamFaculty, TeamMember,
    ApplyJobDetail, ApplyForCourseBanner, ApplyForPositionBanner, FooterConfig, FooterLink,
    FAQCategory, FAQItem, DynamicPageContent, NotificationSetting
)
from about.models import (
    TopBanner as AboutTopBanner, AboutBanner as AboutIntroBanner, AboutManifestoDifferentiator,
    AboutVisionTitle, AboutVisionBanner, AboutVisionItems, CoreValuesTitle, CoreValuesBanner,
    AboutMetric, LeadershipTitle, LeadershipBanner, AchievementTitle, AchievementBanner,
    CampusTitle as AboutCampusTitle, CampusOverview, VisionResearchTitle, VisionResearchBanner,
    LearnMoreContact
)

logger = logging.getLogger('django')

# ==============================================================================
# CENTRALIZED PATH AND MODEL REVALIDATION MAPPINGS USING MODEL CLASSES
# ==============================================================================
MODEL_REVALIDATION_MAP = {
    # --- GLOBAL SITE CONFIG, NAVBAR, TICKERS & NOTIFICATIONS ---
    SiteGlobalSettings: ['/', '/home', '/about-us', '/apply-now', '/contact-us', '/faqs'],
    NavbarLink: ['/', '/home', '/about-us', '/apply-now', '/contact-us', '/faqs'],
    AnnouncementTickerItem: ['/', '/home', '/about-us', '/apply-now', '/contact-us', '/faqs'],
    EligibilityCalculatorConfig: ['/', '/home'],
    EligibilityStreamOption: ['/', '/home'],
    NotificationSetting: ['/', '/home', '/about-us', '/apply-now', '/contact-us', '/faqs'],

    # --- HOME APP CMS MODELS & ISOLATED SHOWCASE ---
    HomeTopBanner: ['/', '/home'],
    HeroTechnicalTag: ['/', '/home'],
    LandingStat: ['/', '/home'],
    AboutBannerTitle: ['/', '/about-us'],
    AboutBanner: ['/', '/about-us'],
    ProgramTitle: ['/', '/programs'],
    Program: ['/', '/programs'],
    IsolatedHomeShowcaseCard: ['/', '/home'],
    IsolatedHomeShowcaseSummaryPoint: ['/', '/home'],
    IsolatedHomeShowcaseFeature: ['/', '/home'],
    IsolatedHomeShowcaseRequirementRule: ['/', '/home'],
    HomeCampusTitle: ['/', '/about-us'],
    CampusFacility: ['/', '/about-us'],
    NewsTitle: ['/'],
    NewsEvent: ['/'],
    AdmissionContactDetail: ['/'],
    AdmissionDetailTitle: ['/'],
    AdmissionCriteria: ['/'],
    TeamTitle: ['/'],
    TeamFaculty: ['/'],
    TeamMember: ['/'],
    ApplyJobDetail: ['/'],
    ApplyForCourseBanner: ['/apply-now'],
    ApplyForPositionBanner: ['/apply-for-job'],
    FooterConfig: ['/', '/home', '/about-us', '/contact-us', '/faqs'],
    FooterLink: ['/', '/home', '/about-us', '/contact-us', '/faqs'],
    FAQCategory: ['/faqs'],
    FAQItem: ['/faqs'],
    DynamicPageContent: ['/privacy-policy', '/terms-and-conditions'],

    # --- ABOUT APP CMS MODELS ---
    AboutTopBanner: ['/about-us'],
    AboutIntroBanner: ['/about-us'],
    AboutManifestoDifferentiator: ['/about-us'],
    AboutVisionTitle: ['/about-us'],
    AboutVisionBanner: ['/about-us'],
    AboutVisionItems: ['/about-us'],
    CoreValuesTitle: ['/about-us'],
    CoreValuesBanner: ['/about-us'],
    AboutMetric: ['/about-us'],
    LeadershipTitle: ['/about-us'],
    LeadershipBanner: ['/about-us'],
    AchievementTitle: ['/about-us'],
    AchievementBanner: ['/about-us'],
    AboutCampusTitle: ['/about-us'],
    CampusOverview: ['/about-us'],
    VisionResearchTitle: ['/about-us'],
    VisionResearchBanner: ['/about-us'],
    LearnMoreContact: ['/about-us'],
}

# ==============================================================================
# CORE UTILITY FUNCTIONS (CACHE INVALIDATION & WEBHOOKS)
# ==============================================================================
def invalidate_cms_cache(app_label=None):
    """
    Clears backend payload cache keys for immediate frontend synchronization.
    """
    keys_to_clear = ['aiems_home_content_payload', 'aiems_about_content_payload']

    for cache_key in keys_to_clear:
        try:
            if cache.delete(cache_key):
                logger.info(f"Backend cache key '{cache_key}' invalidated successfully.")
            else:
                logger.debug(f"Cache key '{cache_key}' was empty or not found during invalidation.")
        except Exception as e:
            logger.error(f"Failed to clear cache key '{cache_key}': {str(e)}")


def fire_revalidation_webhook(paths, model_name=None):
    """
    Triggers an HTTP On-Demand Revalidation call to the Next.js frontend API.
    """
    url = config("FRONTEND_REVALIDATE_URL", default=None)
    secret = config("FRONTEND_REVALIDATE_SECRET", default=None)
    method = config("FRONTEND_REVALIDATE_METHOD", default="POST").upper()

    if not url:
        logger.debug("FRONTEND_REVALIDATE_URL environment variable is not defined. Webhook skipped.")
        return

    def worker():
        try:
            headers = {'User-Agent': 'AIEMS-CMS-Signals/1.0'}

            if method == "POST":
                headers['Content-Type'] = 'application/json'
                payload = {
                    'secret': secret,
                    'paths': list(paths),
                    'model': model_name
                }
                data = json.dumps(payload).encode('utf-8')
                req = urllib.request.Request(url, data=data, headers=headers, method='POST')

                with urllib.request.urlopen(req, timeout=5) as response:
                    status_code = response.getcode()
                    logger.info(f"Frontend ODR webhook success (POST). Status: {status_code}, Paths: {paths}")
            else:
                for path in paths:
                    query_params = {
                        'secret': secret,
                        'path': path
                    }
                    query_params = {k: v for k, v in query_params.items() if v is not None}
                    encoded_params = urllib.parse.urlencode(query_params)

                    get_url = f"{url}?{encoded_params}" if "?" not in url else f"{url}&{encoded_params}"
                    req = urllib.request.Request(get_url, headers=headers, method='GET')

                    with urllib.request.urlopen(req, timeout=5) as response:
                        logger.info(f"Frontend ODR webhook success (GET). Status: {response.getcode()}, Path: {path}")

        except Exception as ex:
            logger.error(f"Frontend ODR webhook invocation failed. Model: {model_name}. Context: {str(ex)}")

    thread = threading.Thread(target=worker, daemon=True)
    thread.start()

# ==============================================================================
# UNIFIED SIGNAL HANDLER IMPLEMENTATION
# ==============================================================================
def handle_cms_content_change(sender, instance, **kwargs):
    """
    Unified signal handler triggered whenever a monitored CMS model changes.
    """
    if kwargs.get('raw', False):
        return

    app_label = sender._meta.app_label
    model_name = sender._meta.model_name

    invalidate_cms_cache(app_label)

    paths = set(MODEL_REVALIDATION_MAP.get(sender, []))

    try:
        if sender == Program and getattr(instance, 'id', None):
            paths.add(f'/programs/{instance.id}')
    except Exception as e:
        logger.debug(f"Dynamic route revalidation mapping extraction bypassed: {str(e)}")

    if paths:
        fire_revalidation_webhook(paths, model_name=sender.__name__)

# ==============================================================================
# SIGNAL REGISTRATION
# ==============================================================================
for model_class in MODEL_REVALIDATION_MAP.keys():
    label = model_class._meta.label
    uid_save = f"revalidate_save_{label}"
    uid_delete = f"revalidate_delete_{label}"

    post_save.connect(
        handle_cms_content_change, 
        sender=model_class, 
        dispatch_uid=uid_save
    )
    post_delete.connect(
        handle_cms_content_change, 
        sender=model_class, 
        dispatch_uid=uid_delete
    )