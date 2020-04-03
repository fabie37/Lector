import itertools as itt
import os
import random
import typing as t
from datetime import timedelta

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lector.settings')
django.setup()

from django.db.models import Model
from lector_app.models import Book, Author, User, UserProfile, Recording


def populate():
    books = [
        {'title': 'Animal Farm',
         'author': {'first_name': 'George', 'last_name': 'Orwell'}},
        {'title': 'A Game Of Thrones (A Song of Ice and Fire – Book 1)',
         'author': {'first_name': 'George', 'last_name': 'R.R. Martin'}},
        {'title': 'Harry Potter and The Chamber of Secrets',
         'author': {'first_name': 'J.K.', 'last_name': 'Rowling'}},
        {'title': 'Notes from Underground',
         'author': {'first_name': 'Fyodor', 'last_name': 'Dostoevsky'}},
        {'title': 'À la recherche du temps perdu',
         'author': {'first_name': 'Marcel', 'last_name': 'Proust'}},
        {'title': 'Pride and Prejudice',
         'author': {'first_name': 'Jane', 'last_name': 'Austen'}},
        {'title': 'The Little Prince',
         'author': {'first_name': 'Antoine', 'last_name': 'de Saint-Exupéry'}},
    ]

    users = [
        {'username': 'reader0', 'first_name': 'Sarah', 'last_name': 'Jane',
         'email': 'someone@xample.com'},
        {'username': 'reader1', 'first_name': 'John', 'last_name': 'Smith',
         'email': 'someone@xample.com'},
        {'username': 'reader2', 'first_name': 'Bill', 'last_name': 'McNab',
         'email': 'someone@xample.com'},
        {'username': 'reader3', 'first_name': 'Mary', 'last_name': 'Sween',
         'email': 'someone@xample.com'},
        {'username': 'reader4', 'first_name': 'Jerôme', 'last_name': 'Allard',
         'email': 'someone@xample.com'}
    ]

    profiles = [{'user': users[0], 'voice_type': 'italian female voice'},
                {'user': users[1], 'voice_type': 'gentle male voice'},
                {'user': users[2], 'voice_type': 'scots voice'},
                {'user': users[3], 'voice_type': 'english voice'},
                {'user': users[4], 'voice_type': 'french voice'}]

    rand = random.Random(42)

    recordings = [{'book': book, 'reader': reader, 'audio_file': 'sample.mp3',
                   'duration': timedelta(seconds=rand.randint(60 * 30, 60 * 150))}
                  for book, reader in itt.product(books[:-1], profiles[:-1])]
    recordings.extend([
        {'book': books[-1], 'reader': profiles[-1], 'duration': timedelta(hours=3, minutes=55),
         'audio_file': 'sample.mp3'}
    ])

    for book in books:
        book['author'] = add_entry(Author, book['author'])
        add_entry(Book, book)

    for profile in profiles:
        profile['user'] = add_user(profile['user'])
        add_entry(UserProfile, profile)

    for recording in recordings:
        recording['book'] = add_entry(Book, recording['book'])
        recording['reader'] = add_entry(UserProfile, recording['reader'])
        add_entry(Recording, recording)


def add_user(data: t.Dict[str, t.Any]):
    qset = User.objects.filter(username=data['username'])
    if not qset.exists():
        user = User.objects.create_user(**data)
        user.save()
        print(f"Created a new user: {user}")
    else:
        user = qset.first()
        print(f"User already existed: {user}")
    return user


def add_entry(model: t.Type[Model], data: t.Dict[str, t.Any]):
    entry, created = model.objects.get_or_create(**data)
    entry.save()
    print(f"Added a new instance of {model.__name__}: {entry}" if created else
          f"Entry already existed: {entry}")
    return entry


if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()
