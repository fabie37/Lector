import typing as t

import whoosh
import whoosh.qparser as qparser
from django.conf import settings
from django.db.models import Model
from whoosh import fields
from whoosh.fields import Schema
from whoosh.index import Index
from whoosh.qparser import QueryParser
from whoosh.writing import AsyncWriter

from .utils import mkdir, pre_call_hook

PK_FIELDTYPE = whoosh.fields.ID(stored=True, unique=True)


class AbstractSearchEngine:
    # fields (instance attributes):
    model: t.Type[Model]  # model whose instances are to be searched
    schema: Schema  # search field schema
    index: Index  # search index
    query_parser: QueryParser  # query parser

    def __init__(self, model: t.Type[Model], schema: Schema, index_name: t.Optional[str] = None):
        """
        :param model: django.db.models.Model subclass whose instances are to be searched
        :param schema: field schema for the search index
        :param index_name: name of the search index
        :param pk_name: field name of the model's primary key
        """
        self.model = model
        self.schema = schema
        self.pk_name = model._meta.pk.name
        self.schema.add(self.pk_name, PK_FIELDTYPE)
        self.index = self._init_index(index_name)
        query_fields = set(schema.names()) - {self.pk_name}
        self.query_parser = LectorQueryParser(query_fields, self.schema)

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
        raise NotImplementedError("subclasses should implement extract_search_fields")

    @pre_call_hook(_check_instance)
    def index(self, instance: Model):
        """Add an entry to the index. Non-blocking."""
        return self.reindex(instance)

    @pre_call_hook(_check_instance)
    def reindex(self, instance: Model):
        """Update an entry in the index. Non-blocking."""
        with AsyncWriter(self.index) as writer:
            writer.update_document(**self._extract_search_fields(instance))

    @pre_call_hook(_check_instance)
    def remove(self, instance: Model):
        """Remove an entry from the index. Non-blocking."""
        with AsyncWriter(self.index) as writer:
            writer.delete_by_term(self.pk_name, getattr(instance, self.pk_name))

    def reindex_all(self, timeout=0.5):
        """Reset the index and index all instances of ``self.model``. Blocking operation."""
        with self.index.writer(timeout=timeout) as writer:
            for instance in self.model.objects.all():
                writer.add_document(**self._extract_search_fields(instance))
            writer.mergetype = whoosh.writing.CLEAR

    def _init_index(self, name: str) -> Index:
        """Initialise the empty index"""
        mkdir(settings.SEARCH_INDEX_DIR)
        self.index = whoosh.index.create_in(settings.SEARCH_INDEX_DIR, self.schema, indexname=name)
        return self.index

    def _extract_search_fields(self, instance: Model) -> t.Dict[str, str]:
        """Internal wrapper around abstract method extract_search_fields"""
        field_values = self.extract_search_fields(instance)
        field_values.setdefault(self.pk_name, str(getattr(instance, self.pk_name)))
        return field_values


class LectorQueryParser(QueryParser):
    """The search query parser for the Lector app"""

    def __init__(self, fieldnames: t.Iterable[str], schema: Schema):
        from whoosh.qparser.plugins import MultifieldPlugin

        super(LectorQueryParser, self).__init__(None, schema, group=qparser.OrGroup)
        self.add_plugin(MultifieldPlugin(fieldnames))
