from typing import *

import language_tags
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from langcodes import Language


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

    def to_python(self, value: Union[Language, str, None]) -> Optional[Language]:
        if value is None or isinstance(value, Language):
            return value
        # `value` is a language tag; parse it:
        return Language.get(value)

    def get_prep_value(self, value: Language) -> str:
        return value.to_tag()


# ----- Models -----

User: Type[models.Model] = settings.AUTH_USER_MODEL


class ReaderProfile(User):
    voice_type = models.CharField(64)
    # languages


class Author(models.Model):
    firstName = models.CharField(32)
    lastName = models.CharField(32)


class Book(models.Model):
    title = models.CharField(128)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)


class Recording(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reader = models.ForeignKey(ReaderProfile, on_delete=models.CASCADE)
    duration = models.IntegerField


class ListenerProfile(User):
    library = models.ManyToManyField(Recording)
