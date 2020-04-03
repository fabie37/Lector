import logging

from django.apps import AppConfig
from django.db.utils import DatabaseError


logger = logging.getLogger('lector-app config')


class LectorAppConfig(AppConfig):
    name = 'lector_app'
    label = 'lector-app'
    verbose_name = 'Lector App'

    def ready(self):
        try:
            from .models import Recording
            Recording.search_engine.reindex_all()
        except DatabaseError as error:
            logger.error(f"database error while loading {self.label} (MIGRATE ASAP): {error}")
