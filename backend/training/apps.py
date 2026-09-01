import logging
import sys
from django.apps import AppConfig

logger = logging.getLogger('django')

class TrainingConfig(AppConfig):
    """
    AppConfig for the AIEMS 'training' core application.
    Manages the lifecycle, startup validation, and safe integration
    for non-technical IT & AI training and lead generation.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'training'
    verbose_name = 'AIEMS IT & AI Training Core'

    def ready(self):
        is_managing = 'manage.py' in sys.argv or 'django-admin' in sys.argv
        is_migration = any(cmd in sys.argv for cmd in ['migrate', 'makemigrations', 'showmigrations', 'sqlmigrate'])
        is_testing = 'test' in sys.argv

        logger.debug(
            f"Initializing AIEMS Training AppConfig (Runtime context: "
            f"manage={is_managing}, migration={is_migration}, test={is_testing})"
        )
        logger.info("AIEMS IT & AI Training CMS registry initialization complete.")