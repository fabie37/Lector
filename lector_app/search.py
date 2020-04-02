import typing as t

import whoosh.fields
import whoosh.writing
from django.conf import settings
from django.db.models import Model
from whoosh.fields import Schema
from whoosh.index import Index, create_in

from .utils import mkdir, pre_call_hook


class AbstractSearchFunctionality:
    PK_FIELDTYPE = whoosh.fields.ID(stored=True, unique=True)

    # fields (instance attributes):
    model: t.Type[Model]
    schema: Schema
    index: Index
    name: str

    def __init__(self, model: t.Type[Model], schema: Schema,
                 pk_name: str = 'id', name: t.Optional[str] = None):
        """
        :param model: django.db.models.Model subclass whose instances are to be searched
        :param schema: field schema for the search index
        :param name: name of the search index
        :param pk_name: field name of the model's primary key
        """
        self.model = model
        self.schema = schema
        self.schema.add(pk_name, AbstractSearchFunctionality.PK_FIELDTYPE)
        self.pk_name = pk_name
        self.name = name
        self.index = self._create_index()
        self._buffered_writer = whoosh.writing.BufferedWriter(self.index)

    def _create_index(self) -> Index:
        """Initialise the empty index"""
        mkdir(settings.SEARCH_INDEX_DIR)
        self.index = create_in(settings.SEARCH_INDEX_DIR, self.schema, indexname=self.name)
        return self.index

    def _check_instance(self, instance: Model):
        if not isinstance(instance, self.model):
            raise TypeError(f"expected an instance of {self.model}")

    @pre_call_hook(_check_instance)
    def extract_search_fields(self, instance: Model) -> t.Dict[str, str]:
        """
        Subclasses should override this to implement extraction of search index fields (as
        specified by ``self.schema``) from an object that needs to be indexed. The base
        implementation just makes some checks and extracts the primary key.

        :param instance: object to be indexed; should be an instance of ``self.model``
        :return: a dictionary mapping index field names to values
        """
        return {self.pk_name: getattr(instance, self.pk_name)}

    @pre_call_hook(_check_instance)
    def index(self, instance: Model):
        """Add an entry to the index"""
        return self.reindex(instance)

    @pre_call_hook(_check_instance)
    def reindex(self, instance: Model):
        """Update an entry in the index"""
        self._buffered_writer.update_document(**self.extract_search_fields(instance))

    @pre_call_hook(_check_instance)
    def remove(self, instance: Model):
        """Remove an entry from the index"""
        self._buffered_writer.delete_by_term(self.pk_name, instance.id)

    def reindex_all(self):
        """Reset the index and index all instances of ``self.model``"""
        with self._buffered_writer as writer:
            for instance in self.model.objects.all():
                writer.add_document(**self.extract_search_fields(instance))
            writer.mergetype = whoosh.writing.CLEAR

    def __del__(self):
        self._buffered_writer.close()


class RecordingSearch(AbstractSearchFunctionality):
    from .models import Recording

    model = Recording
    schema = Schema(book_title=whoosh.fields.TEXT(spelling=True),
                    author_name=whoosh.fields.TEXT(spelling=True),
                    reader_name=whoosh.fields.TEXT(spelling=True))

    def __init__(self, name: t.Optional[str] = None):
        super().__init__(RecordingSearch.model, RecordingSearch.schema, name=name)

    def extract_search_fields(self, recording: Recording) -> t.Dict[str, str]:
        super().extract_search_fields(recording)
        book, author, reader = recording.book, recording.book.author, recording.reader
        fields = dict(book_title=book.title,
                      author_name=author.full_name,
                      reader_name=reader.full_name)
        return {k: str(v) for k, v in fields.items()}


RECORDING_SEARCH = RecordingSearch()
