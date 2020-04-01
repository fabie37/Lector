import typing as t

import whoosh
from django.conf import settings
from django.db.models import Model
from whoosh.fields import Schema
from whoosh.index import Index, create_in

from .utils import mkdir


class AbstractSearchFunctionality:
    model: t.Type[Model]
    schema: Schema
    index: Index
    name: str

    def __init__(self, model: t.Type[Model], schema: Schema, name: t.Optional[str] = None):
        """
        :param model: django.db.models.Model subclass whose instances are to be searched
        :param schema: field schema for the search index
        :param name: name of the search index
        """
        self.model = model
        self.schema = schema
        self.name = name

    def extract_search_fields(self, instance: Model) -> t.Dict[str, str]:
        """
        Subclasses should override this to implement extraction of search index fields (as
        specified by ``self.schema``) from an
        object that needs to be indexed.

        :param instance: object to be indexed; should be an instance of ``self.model``
        :return: a dictionary mapping index field names to values
        """
        if not isinstance(instance, self.model):
            raise TypeError(f"expected an instance of {self.model}")
        raise NotImplementedError("should be overridden in subclasses")

    def create_index(self) -> Index:
        """Initialise the empty index"""
        mkdir(settings.SEARCH_INDEX_DIR)
        self.index = create_in(settings.SEARCH_INDEX_DIR, self.schema, indexname=self.name)
        return self.index

    def index_all(self):
        """Index all instances of ``self.model``"""
        writer = self.index.writer()
        for instance in self.model.objects.all():
            writer.add_document(**self.extract_search_fields(instance))


class RecordingSearch(AbstractSearchFunctionality):
    from .models import Recording

    model = Recording
    schema = Schema(id=whoosh.fields.ID(stored=True),
                    book_title=whoosh.fields.TEXT(spelling=True),
                    author_name=whoosh.fields.TEXT(spelling=True),
                    reader_name=whoosh.fields.TEXT(spelling=True))

    def __init__(self, name: t.Optional[str] = None):
        super().__init__(RecordingSearch.model, RecordingSearch.schema, name=name)

    def extract_search_fields(self, recording: Recording) -> t.Dict[str, str]:
        super().extract_search_fields(recording)
        book, author, reader = recording.book, recording.book.author, recording.reader
        return dict(id=recording.id,
                    book_title=book.title,
                    author_name=' '.join((author.firstName, author.lastName)),
                    reader_name=' '.join((reader.first_name, reader.last_name)))


RECORDING_SEARCH = RecordingSearch()
