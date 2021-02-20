from django.contrib.auth.models import User
from django.test import TestCase

from library.models import Author


class AuthorTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Author.objects.create(first_name='Александр', last_name='Пушкин', birth_year=1799)
        Author.objects.create(first_name='Николай', last_name='Гоголь', birth_year=1809)
        Author.objects.create(first_name='Виктор', last_name='Пелевин', birth_year=1962, is_active=False)

        User.objects.create_user('user', password='Qwerty123', is_staff=True)

    def test_get_all_authors(self):
        response = self.client.get('/api/authors/')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()['results']
        self.assertEqual(len(response_json), 2)
        self.assertEqual(response_json[0]['first_name'], 'Александр')
        self.assertEqual(response_json[1]['first_name'], 'Николай')

    def test_post_author(self):
        self.client.login(username='user', password='Qwerty123')
        data = {
            "first_name": "Михаил",
            "last_name": "Лермонтов",
            "birth_year": 1814
        }
        response = self.client.post('/api/authors/', data=data)
        self.assertEqual(response.status_code, 201)
        authors = Author.objects.all()
        self.assertEqual(len(authors), 4)
        self.assertEqual(authors[3].first_name, 'Михаил')

    def test_get_author_by_name(self):
        response = self.client.get('/api/authors/?name=Пушкин')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()['results']
        self.assertEqual(len(response_json), 1)
        self.assertEqual(response_json[0]['first_name'], 'Александр')

    def test_get_author_by_full_name(self):
        response = self.client.get('/api/authors/?name=Александр Пушкин')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()['results']
        self.assertEqual(len(response_json), 1)
        self.assertEqual(response_json[0]['first_name'], 'Александр')

    def test_set_active(self):
        self.client.login(username='user', password='Qwerty123')
        response = self.client.get('/api/authors/?name=Пелевин')
        response_json = response.json()['results']
        self.assertEqual(len(response_json), 0)

        data = {"value": "true"}
        response = self.client.post('/api/authors/3/set_active/', data=data)
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/api/authors/?name=Пелевин')
        response_json = response.json()['results']
        self.assertEqual(len(response_json), 1)
