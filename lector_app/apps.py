import logging

from django.apps import AppConfig
from django.db.utils import OperationalError


class LectorAppConfig(AppConfig):
    name = 'lector_app'
    label = 'lector-app'
    verbose_name = 'Lector App'

    def ready(self):
        try:
            from .search import RECORDING_SEARCH
            RECORDING_SEARCH.reindex_all()
        except OperationalError as error:
            logging.exception(f"OperationalError while loading {self.label} (try migrating first)",
                              exc_info=error)
