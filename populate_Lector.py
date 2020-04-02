import os
import typing as t

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lector.settings')
django.setup()

from lector_app.models import Book, Author, Model


def populate():
    books = [
        {'title': 'Animal Farm',
         'author': {'first_name': 'George', 'last_name': 'Orwell'}},
        {'title': 'A Game Of Thrones (A Song of Ice and Fire Book 1)',
         'author': {'first_name': 'George', 'last_name': 'R.R. Martin'}},
        {'title': 'Harry Potter and The Chamber of Secrets',
         'author': {'first_name': 'J.K.', 'last_name': 'Rowling'}},
    ]

    for book in books:
        book['author'] = add_entry(Author, book['author'])
        add_entry(Book, book)


def add_entry(model: t.Type[Model], data: t.Dict[str, t.Any]):
    entry, created = model.objects.get_or_create(**data)
    entry.save()
    print(f"Added a new instance of {model.__name__}: {entry}" if created else
          f"Entry already existed: {entry}")
    return entry


if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()
