from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from library.models import Books
from library.serializers import BooksSerializer
from .test_author import sample_author

BOOKS_URL = reverse('books-list')


def detail_url(book_id):
    return reverse('books-detail', args=[book_id])


def sample_book(**params):
    defaults = {
        'title': 'book1',
        'book_pages': 23,
        'genre': 1,
        'release_date': '2023-01-01',
    }
    defaults.update(params)
    book = Books.objects.create(**defaults)
    book.author.add(sample_author(name='test2'))
    return book


class BooksViewTests(TestCase):
    maxDiff = None
    # fixtures = [
    #     "author.json",
    #     "books.json",
    # ]

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='test',
            password='123456'
        )
        self.client.force_authenticate(self.user)
        self.unauthorized_client = APIClient()

    def test_list_view_unauthorized_read_only(self):
        sample_book()
        response = self.unauthorized_client.get(BOOKS_URL)

        book = Books.objects.all()
        serializer = BooksSerializer(book, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(response.data), 1)

    def test_detail_view_unauthorized_read_only(self):
        book = sample_book()
        url = detail_url(book.id)
        response = self.unauthorized_client.get(url)

        serializer = BooksSerializer(book)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_unauthorized(self):
        payload = {
            'title': 'book1',
            'book_pages': 23,
            'genre': 1,
            'release_date': '2023-01-01',
        }
        response = self.unauthorized_client.post(BOOKS_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_view(self):
        sample_book()
        response = self.client.get(BOOKS_URL)

        books = Books.objects.all()
        serializer = BooksSerializer(books, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(response.data), 1)

    def test_detail_view(self):
        book = sample_book()
        url = detail_url(book.id)
        response = self.client.get(url)

        serializer = BooksSerializer(book)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create(self):
        payload = {
            'title': 'book2',
            'book_pages': 50,
            'genre': 1,
            'author': [sample_author().id],
            'release_date': '2023-01-01',
        }
        response = self.client.post(BOOKS_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], payload['title'])
        self.assertEqual(response.data['book_pages'], payload['book_pages'])
        self.assertEqual(response.data['genre'], payload['genre'])

    def test_partial_update(self):
        book = sample_book()
        payload = {
            'title': 'book3',
            'book_pages': 90,
        }
        url = detail_url(book.id)
        self.client.patch(url, payload)
        book.refresh_from_db()
        self.assertEqual(book.title, payload['title'])
        self.assertEqual(book.book_pages, payload['book_pages'])

    def test_full_update(self):
        book = sample_book()
        payload = {
            'title': 'book4',
            'book_pages': 70,
            'genre': 1,
            'author': [sample_author().id],
            'release_date': '2023-02-01',
        }
        url = detail_url(book.id)
        self.client.put(url, payload)
        book.refresh_from_db()
        self.assertEqual(book.title, payload['title'])
        self.assertEqual(book.book_pages, payload['book_pages'])
        self.assertEqual(book.genre, payload['genre'])

    def test_delete(self):
        book = sample_book()
        self.assertTrue(
            Books.objects.filter(id=book.id).exists()
        )

        url = detail_url(book.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Books.objects.filter(id=book.id).exists())

    def test_search_by_title(self):
        book = sample_book()
        response = self.client.get(BOOKS_URL + f'?search={book.title}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.json()),
            Books.objects.filter(title=book.title).count()
        )

    def test_search_by_author(self):
        sample_book()
        response = self.client.get(BOOKS_URL + f'?search=test2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.json()),
            Books.objects.filter(author__name='test2').count()
        )

    def test_search_by_book_pages(self):
        book = sample_book()
        response = self.client.get(BOOKS_URL + f'?search={book.book_pages}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.json()),
            Books.objects.filter(book_pages=book.book_pages).count()
        )

    def test_search_by_release_date(self):
        book = sample_book()
        response = self.client.get(BOOKS_URL + f'?search={book.book_pages}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.json()),
            Books.objects.filter(book_pages=book.book_pages).count()
        )

    def test_search_by_release_date(self):
        sample_book()
        response = self.client.get(BOOKS_URL + f'?search=2023-01-01')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.json()),
            Books.objects.filter(release_date='2023-01-01').count()
        )
