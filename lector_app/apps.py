from django.apps import AppConfig


class LectorAppConfig(AppConfig):
    name = 'lector_app'
    label = 'lector-app'
    verbose_name = 'Lector App'

    def ready(self):
        from .search import RECORDING_SEARCH
        RECORDING_SEARCH.reindex_all()
