from django.apps import AppConfig

from .search import RECORDING_SEARCH


class LectorAppConfig(AppConfig):
    name = 'lector_app'
    label = 'lector-app'
    verbose_name = 'Lector App'

    def ready(self):
        super().ready()
        RECORDING_SEARCH.create_index()
        RECORDING_SEARCH.index_all()
