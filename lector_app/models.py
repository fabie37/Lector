from typing import *

import language_tags
from django.contrib.auth.models import User
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


class ReaderProfile(User):
    voice_type = models.CharField(max_length=64)
    # languages


class Author(models.Model):
    firstName = models.CharField(max_length=32)
    lastName = models.CharField(max_length=32)


class Book(models.Model):
    title = models.CharField(max_length=128)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)


class Recording(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reader = models.ForeignKey(ReaderProfile, on_delete=models.CASCADE)
   # duration = models.IntegerField
    mp3file=models.FileField(upload_to=str(ReaderProfile)+'library/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.book + " by " + self.reader

    def delete(self, *args, **kwargs):
        self.mp3file.delete()
        super().delete(*args, **kwargs)


class ListenerProfile(User):
    library = models.ManyToManyField(Recording)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
