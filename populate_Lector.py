import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lector.settings')

import django
django.setup()
from lector_app.models import Book, Author


def populate():
    book_details = [
    {'title' : 'Animal Farm'},   
    {'title' : 'A Game Of Thrones (A Song of Ice and Fire Book 1)'},
    {'title' : 'Harry Potter and The Chamber of Secrets'}]
    
    author_details = [
    {'name':'George',
    'surname' : 'Orwell'},
    {'name' : 'George',
    'surname'  : 'R.R. Martin'}, 
    {'name' : 'J.K.',
    'surname' : 'Rowling'}]
    
    cats = {'My Library': {'books': book_details}, 
           'Authors': {'authors': author_details}}
    
    for cat, cat_data in cats.items():
        x = add_auth(cats[cat]['Authors']['authors']['name'], cats[cat]['Authors']['authors']['surname'])
        for c in cat_data['books']:
            add_book(x, c['title'], c['author'])
            
    for book, author in zip(books, authors):
        for b in Book.objects.filter(category=c):
            print(f'- {a}: {b}')
            
def add_book(cat, title, author):
    b = Book.objects.get_or_create(title=title,author=author)[0]
    b.save()
    return b
    
def add_auth(name, surname):
    a = Author.objects.get_or_create(name=name, surname=surname)[0]
    a.save()
    return a

if __name__ == '__main__': 
    print('Starting Rango population script...') 
    populate()      