from django.contrib.auth.models import User
from django.test import TestCase

from library.models import Author, Book


class BookTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        author = Author.objects.create(first_name='Александр', last_name='Пушкин', birth_year=1799)
        Book.objects.create(title='Евгений Онегин', author=author, isbn=123456789,
                            publication_year=1833, sheets_number=300)
        Book.objects.create(title='Капитанская дочка', author=author, isbn=789456123,
                            publication_year=1836, sheets_number=600)

        author = Author.objects.create(first_name='Николай', last_name='Гоголь', birth_year=1809)
        Book.objects.create(title='Вечера на хуторе близ Диканьки', author=author, isbn=987654321,
                            publication_year=1831, sheets_number=700)
        Book.objects.create(title='Ревизор', author=author, isbn=321654987,
                            publication_year=1836, sheets_number=250)

        User.objects.create_user('user', password='Qwerty123')

    def test_get_all_books(self):
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()['results']
        self.assertEqual(len(response_json), 4)
        self.assertEqual(response_json[0]['title'], 'Евгений Онегин')
        self.assertEqual(response_json[1]['title'], 'Капитанская дочка')

    def test_post_book(self):
        self.client.login(username='user', password='Qwerty123')
        data = {
            "title": "Сказка о царе Салтане",
            "author": 1,
            "isbn": 987654321,
            "publication_year": 1832,
            "sheets_number": 300
        }
        response = self.client.post('/api/books/', data=data)
        self.assertEqual(response.status_code, 201)
        books = Book.objects.all()
        self.assertEqual(len(books), 5)
        self.assertEqual(books[4].title, 'Сказка о царе Салтане')

    def test_get_book_by_author(self):
        response = self.client.get('/api/books/?author=Пушкин')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()['results']
        self.assertEqual(len(response_json), 2)
        self.assertEqual(response_json[0]['title'], 'Евгений Онегин')
        self.assertEqual(response_json[1]['title'], 'Капитанская дочка')

    def test_get_book_by_title(self):
        response = self.client.get('/api/books/?title=Евгений Онегин')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()['results']
        self.assertEqual(len(response_json), 1)
        self.assertEqual(response_json[0]['title'], 'Евгений Онегин')

    def test_get_book_by_pages_number(self):
        response = self.client.get('/api/books/?pages=300')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()['results']
        self.assertEqual(len(response_json), 1)
        self.assertEqual(response_json[0]['title'], 'Евгений Онегин')

    def test_get_book_by_pages_condition(self):
        response = self.client.get('/api/books/?pages=400&operator=lt')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()['results']
        self.assertEqual(len(response_json), 2)
        self.assertEqual(response_json[0]['title'], 'Евгений Онегин')
        self.assertEqual(response_json[1]['title'], 'Ревизор')

    def test_get_book_by_author_and_pages_condition(self):
        response = self.client.get('/api/books/?author=Пушкин&pages=400&operator=lt')
        self.assertEqual(response.status_code, 200)
        response_json = response.json()['results']
        self.assertEqual(len(response_json), 1)
        self.assertEqual(response_json[0]['title'], 'Евгений Онегин')
