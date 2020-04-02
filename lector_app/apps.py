import logging

from django.apps import AppConfig
from django.db.migrations.exceptions import InvalidBasesError
from django.db.utils import DatabaseError


class LectorAppConfig(AppConfig):
    name = 'lector_app'
    label = 'lector-app'
    verbose_name = 'Lector App'

    def ready(self):
        try:
            from .models import Recording
            Recording.indexer.init_index()
            Recording.indexer.reindex_all()
        except (DatabaseError, InvalidBasesError) as error:
            logging.exception(f"database error while loading {self.label} (try migrating first)",
                              exc_info=error)
