from django.contrib import admin

from .models import Author, Book
from .models import UserProfile
from .models import Recording


admin.site.register(Author)
admin.site.register(Book)
admin.site.register(UserProfile)
admin.site.register(Recording)


