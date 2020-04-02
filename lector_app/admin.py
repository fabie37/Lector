from django.contrib import admin

from .models import Author, Book, ListenerProfile, ReaderProfile, Recording, UserProfile


admin.site.register(ReaderProfile)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Recording)
admin.site.register(ListenerProfile)
admin.site.register(UserProfile)
