import typing as t

import language_tags
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from langcodes import Language

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


# ----- Models -----


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


class Recording(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reader = models.ForeignKey(ReaderProfile, on_delete=models.CASCADE)
    duration = models.IntegerField

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
