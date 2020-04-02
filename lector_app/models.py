import language_tags
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.base import ModelBase
from langcodes import Language

from .search import *
from .utils import HasHumanName


# ----- Custom fields -----

def validate_language_tag(value: str):
    if not language_tags.tags.check(value):
        raise ValidationError(f'invalid language tag: {value}')


class LanguageField(models.Field):
    """
    Field representing a natural language variant. Stored on the database as a BCP-47 language
    tag (a CharField, thus), and as a :class:`langcodes.Lanuage` object for its Python
    representation.
    """

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 16
        kwargs['validators'] = [validate_language_tag]
        super().__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'CharField'

    def from_db_value(self, db_value: str, expression, connection) -> Language:
        return self.to_python(db_value)

    def to_python(self, value: t.Union[Language, str, None]) -> t.Optional[Language]:
        if value is None or isinstance(value, Language):
            return value
        # `value` is a language tag; parse it:
        return Language.get(value)

    def get_prep_value(self, value: Language) -> str:
        return value.to_tag()


# ----- Abstract Models & metaclasses -----

class IndexedModelMeta(ModelBase):
    """Metaclass for indexed Models.
    Adds an overridden save() function to the class' definition that re-indexes the saved
    instance after saving.
    Classes with this metaclass should define an inner class ``Indexer`` that is a subclass of
    :class:`lector_app.search.AbstractIndexer`.
    Also adds an ``indexer`` class field to the Model, which is an instance of the model's
    ``Indexer`` inner class.
    """

    def __new__(mcs, name, bases, attrs, **kwargs):
        indexer_class = attrs.pop('Indexer', None)
        if not issubclass(indexer_class, AbstractIndexer):
            raise TypeError(f"indexed model {name} should define an 'Indexer' inner class that is "
                            f"a subclass of AbstractIndexer")

        model = super().__new__(mcs, name, bases, attrs, **kwargs)
        indexer_class.model = model
        indexer = indexer_class()

        def save(self, *args, **kwargs):
            super(model, self).save(*args, **kwargs)
            indexer.reindex(self)

        setattr(model, 'save', save)
        setattr(model, 'indexer', indexer)
        return model


# ----- Concrete Models -----

class ReaderProfile(User, HasHumanName):
    voice_type = models.CharField(max_length=64)

    # TODO: languages

    def __str__(self):
        return f"{self.full_name} ({self.voice_type.lower()})"


class Author(HasHumanName, models.Model):
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)

    def __str__(self):
        return self.full_name


class Book(models.Model):
    title = models.CharField(max_length=128)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}, by {self.author}"


class Recording(models.Model, metaclass=IndexedModelMeta):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reader = models.ForeignKey(ReaderProfile, on_delete=models.CASCADE)
    duration = models.PositiveIntegerField()

    class Indexer(AbstractIndexer):
        def __init__(self):
            schema = Schema(book_title=whoosh.fields.TEXT(spelling=True),
                            author_name=whoosh.fields.TEXT(spelling=True),
                            reader_name=whoosh.fields.TEXT(spelling=True))
            super().__init__(self.model, schema, index_name='lector-app.Recording')

        def extract_search_fields(self, recording: 'Recording') -> t.Dict[str, str]:
            book, author, reader = recording.book, recording.book.author, recording.reader
            return dict(book_title=book.title, author_name=author.full_name,
                        reader_name=reader.full_name)

    def __str__(self):
        return f"{self.book.title}, by {self.book.author} – narrated by {self.reader}"


class ListenerProfile(User, HasHumanName):
    library = models.ManyToManyField(Recording)

    def __str__(self):
        return self.full_name


class UserProfile(models.Model, HasHumanName):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name
