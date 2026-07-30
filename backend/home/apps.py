import logging
import sys
from django.apps import AppConfig

logger = logging.getLogger('django')

class HomeConfig(AppConfig):
    """
    AppConfig for the AIEMS 'home' core application.
    Manages the application lifecycle, safe initialization, defensive signal registration,
    and verifies backend system status without disrupting migrations, tests, or management commands.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'
    verbose_name = 'AIEMS Home CMS Core'

    def ready(self):
        """
        Executed when the application registry is fully populated.
        Performs safe initialization logic, registers signal handlers,
        and verifies backend availability while ensuring context safety.
        """
        # 1. Identify runtime context to prevent running heavy logic or failing during database migrations/tests
        is_managing = 'manage.py' in sys.argv or 'django-admin' in sys.argv
        is_migration = any(cmd in sys.argv for cmd in ['migrate', 'makemigrations', 'showmigrations', 'sqlmigrate'])
        is_testing = 'test' in sys.argv

        logger.debug(
            f"Initializing AIEMS Home AppConfig (Runtime context: "
            f"manage={is_managing}, migration={is_migration}, test={is_testing})"
        )

        # 2. Defensive Signal Registration
        # Safely imports the signals module only after the registry is ready,
        # preventing circular imports or premature database model interactions.
        try:
            import home.signals  # noqa: F401
            logger.info("Successfully registered signal handlers for the 'home' core application.")
        except ImportError as e:
            # If signals.py does not exist, log a debug message without breaking startup.
            # If it failed due to a different import error, log a warning with the traceback.
            if "No module named 'home.signals'" in str(e):
                logger.debug("No custom signals module found for 'home' application.")
            else:
                logger.warning(
                    f"Signals module import failed inside 'home' application. Details: {str(e)}",
                    exc_info=True
                )

        # 3. Connection Diagnostics & Cache Backend Validation
        # Verify cache connectivity defensively only when the application is running in an active server state
        if not is_migration and not is_testing:
            self._verify_cache_backend()

    def _verify_cache_backend(self):
        """
        Defensively tests connectivity to the configured cache backend at startup.
        Ensures high availability in production without running blocking database transactions.
        """
        try:
            # Lazy import to prevent premature loading before Django is fully configured
            from django.core.cache import cache

            cache.set('aiems_startup_connectivity_probe', True, timeout=5)
            probe_success = cache.get('aiems_startup_connectivity_probe')
            
            if probe_success:
                logger.info("AIEMS Core Cache backend connectivity verified successfully.")
            else:
                logger.warning("Cache backend connectivity probe returned an unexpected empty response.")
        except Exception as e:
            # Prevents hard failures if the cache backend is temporarily offline during zero-downtime deployments
            logger.error(
                f"Defensive cache verification failed during application startup. "
                f"Falling back to un-cached operations. Error context: {str(e)}"
            )