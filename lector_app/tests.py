import random
import string
import unittest

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from . import models


# # models test
class ModelsTests(TestCase):

    def test_book_and_author_toString(self):
        sampler = models.Author(first_name="Adam", last_name="Sampler")
        diary = models.Book(title="Struggle with Django", author=sampler)
        self.assertEqual(str(diary) == ('Struggle with Django, by Adam Sampler'), True)

    def test_baselogin(self):
        self.random_username = ''.join(random.choices(string.ascii_uppercase, k=10))
        self.client = Client()
        self.user = User.objects.create_user(self.random_username, 'sad@thebeatles.com', 'johnpassword')
        self.client.login(username=self.random_username, password='johnpassword')

        self.response_login = self.client.get(reverse('lector-app:login'))

        self.assertTemplateUsed(self.response_login, 'lector-app/base.html')


class LoginTestCase(unittest.TestCase):
    def setUp(self):
        self.random_username = ''.join(random.choices(string.ascii_uppercase, k=10))
        self.client = Client()
        self.user = User.objects.create_user(self.random_username, 'sad@thebeatles.com', 'johnpassword')

    def testSignUpDublicate(self):
        catches = False
        try:
            self.user = User.objects.create_user(self.random_username, 'sad@thebeatles.com', 'johnpassword')
        except Exception as e:
            catches = True
        self.assertEqual(catches, True)  # Catches dublicate

    def testLogin(self):
        self.client.login(username=self.random_username, password='johnpassword')
        self.login_url = reverse('lector-app:login')
        response = self.client.post(self.login_url, follow=True)
        self.assertEqual(response.status_code, 200)

    def testLogout(self):
        self.client.login(username=self.random_username, password='johnpassword')
        self.logout_url = reverse('lector-app:logout')
        response = self.client.post(self.logout_url, follow=True)
        self.assertEqual(response.status_code, 200)
