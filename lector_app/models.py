import typing as t

from django.contrib.auth.models import User
from django.db import models
from django.db.models.base import ModelBase

from . import search
from .utils import HasHumanName


# ----- Abstract Models & metaclasses -----

class IndexedModelMeta(ModelBase):
    """Metaclass for indexed Models.
    Adds an overridden save() function to the class' definition that re-indexes the saved
    instance after saving.
    Classes with this metaclass should define an inner class ``SearchEngine`` that is a subclass of
    :class:`lector_app.search.AbstractSearchEngine`.
    Also adds a ``search_engine`` class field to the Model, which is an instance of the model's
    ``SearchEngine`` inner class.

    A metaclass is needed to intercept the model class creation before the django model metaclass
    gobbles up all class attributes.
    """

    def __new__(mcs, name, bases, attrs, **kwargs):
        search_engine_class = attrs.pop('SearchEngine', None)
        if not issubclass(search_engine_class, search.AbstractSearchEngine):
            raise TypeError(
                f"indexed model {name} should define an 'SearchEngine' inner class that is "
                f"a subclass of .search.AbstractSearchEngine")

        model = super().__new__(mcs, name, bases, attrs, **kwargs)
        search_engine_class.model = model
        search_engine = search_engine_class()

        def save(self, *args, **kwargs):
            super(model, self).save(*args, **kwargs)
            search_engine.reindex(self)

        setattr(model, 'save', save)
        setattr(model, 'search_engine', search_engine)
        return model


# ----- Concrete Models -----
class UserProfile(models.Model, HasHumanName):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    library = models.ManyToManyField('Recording', blank=True)
    voice_type = models.CharField(max_length=64)

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    def __str__(self):
        return f"{self.full_name} ({self.user})"


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
    reader = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    duration = models.DurationField()
    audio_file = models.FileField(upload_to='audio_files/')

    class SearchEngine(search.AbstractSearchEngine):
        def __init__(self):
            schema = search.Schema(book_title=search.fields.TEXT(spelling=True),
                                   author_name=search.fields.TEXT(spelling=True),
                                   reader_name=search.fields.TEXT(spelling=True))
            super().__init__(self.model, schema, index_name='lector-app.Recording')

        def extract_search_fields(self, recording: 'Recording') -> t.Dict[str, str]:
            book, author, reader = recording.book, recording.book.author, recording.reader
            return dict(book_title=book.title, author_name=author.full_name,
                        reader_name=reader.user.username)

    def __str__(self):
        return f"{self.book.title}, by {self.book.author} – narrated by {self.reader}"
