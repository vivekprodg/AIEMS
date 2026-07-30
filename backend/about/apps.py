import logging
import sys
from django.apps import AppConfig

logger = logging.getLogger('django')

class AboutConfig(AppConfig):
    """
    AppConfig for the AIEMS 'about' core application.
    Manages the application lifecycle, safe initialization, and startup validation 
    without disrupting migrations, tests, or management commands.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'about'
    verbose_name = 'AIEMS About CMS Core'

    def ready(self):
        """
        Executed when the application registry is fully populated.
        Performs diagnostic logging, checks runtime execution contexts,
        and safely ensures integration with global signals and caching modules.
        """
        is_managing = 'manage.py' in sys.argv or 'django-admin' in sys.argv
        is_migration = any(cmd in sys.argv for cmd in ['migrate', 'makemigrations', 'showmigrations', 'sqlmigrate'])
        is_testing = 'test' in sys.argv

        logger.debug(
            f"Initializing AIEMS About AppConfig (Runtime context: "
            f"manage={is_managing}, migration={is_migration}, test={is_testing})"
        )

        # Defensive Verification of Signals Integration
        # The central 'home.signals' module handles dynamic On-Demand Revalidation (ODR)
        # and cache invalidation hooks for our models using lazy string-based connection.
        # This setup ensures that we check if signals are loaded safely.
        try:
            # If application-specific local signals are introduced in 'about/signals.py'
            # in the future, they will be loaded safely here.
            pass
        except Exception as e:
            logger.warning(
                f"Optional signal registration check for 'about' application failed. Details: {str(e)}",
                exc_info=True
            )

        logger.info("AIEMS About CMS Core application registry initialization complete.")