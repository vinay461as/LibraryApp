import os
import tempfile
from PIL import Image
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from library.models import Author
from library.serializers import AuthorSerializer

AUTHOR_URL = reverse('author-list')


def detail_url(author_id):
    return reverse('author-detail', args=[author_id])


def image_upload_url(author_id):
    return reverse('author-upload-image', args=[author_id])


def sample_author(**params):
    defaults = {
        "name": "test",
        "surname": "author",
        "email": "test@gmail.com",
        "phone": 9120032100,
        "fb_name": "sn",
    }
    defaults.update(params)
    return Author.objects.create(**defaults)


class AuthorViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='test',
            password='123456'
        )
        self.client.force_authenticate(self.user)
        self.unauthorized_client = APIClient()

    def test_list_view_unauthorized_read_only(self):
        sample_author()
        response = self.unauthorized_client.get(AUTHOR_URL)

        author = Author.objects.all()
        serializer = AuthorSerializer(author, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(response.data), 1)

    def test_detail_view_unauthorized_read_only(self):
        author = sample_author()
        url = detail_url(author.id)
        response = self.unauthorized_client.get(url)

        serializer = AuthorSerializer(author)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_unauthorized(self):
        payload = {
            "name": "test",
            "surname": "author",
            "email": "test@gmail.com",
            "phone": 9120032100,
        }
        response = self.unauthorized_client.post(AUTHOR_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_view(self):
        sample_author()
        response = self.client.get(AUTHOR_URL)

        author = Author.objects.all()
        serializer = AuthorSerializer(author, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(response.data), 1)

    def test_detail_view(self):
        author = sample_author()
        url = detail_url(author.id)
        response = self.client.get(url)

        serializer = AuthorSerializer(author)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create(self):
        payload = {
            "name": "test",
            "surname": "author",
            "email": "test@gmail.com",
            "phone": 9120032100,
        }
        response = self.client.post(AUTHOR_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        author = Author.objects.get(id=response.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(author, key))

    def test_partial_update(self):
        author = sample_author()
        payload = {
            "email": "author@gmail.com",
            "phone": 9000060000,
        }
        url = detail_url(author.id)
        self.client.patch(url, payload)
        author.refresh_from_db()
        self.assertEqual(author.email, payload['email'])
        self.assertEqual(author.phone, payload['phone'])

    def test_full_update(self):
        author = sample_author()
        payload = {
            "name": "test1",
            "surname": "author1",
            "email": "author@gmail.com",
            "phone": 9000000100,
        }
        url = detail_url(author.id)
        self.client.put(url, payload)
        author.refresh_from_db()
        self.assertEqual(author.name, payload['name'])
        self.assertEqual(author.surname, payload['surname'])
        self.assertEqual(author.email, payload['email'])
        self.assertEqual(author.phone, payload['phone'])

    def test_delete(self):
        author = sample_author()
        self.assertTrue(Author.objects.filter(id=author.id).exists())

        url = detail_url(author.id)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Author.objects.filter(id=author.id).exists())

    def test_search_by_name(self):
        author = sample_author()
        response = self.client.get(AUTHOR_URL + f'?search={author.name}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.json()),
            Author.objects.filter(name=author.name).count()
        )

    def test_search_by_email(self):
        author = sample_author()
        response = self.client.get(AUTHOR_URL + f'?search={author.email}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.json()),
            Author.objects.filter(email=author.email).count()
        )

    def test_search_by_surname(self):
        author = sample_author()
        response = self.client.get(AUTHOR_URL + f'?search={author.surname}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.json()),
            Author.objects.filter(surname=author.surname).count()
        )

    def test_upload_image_to_recipe(self):
        author = sample_author()
        url = image_upload_url(author.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            response = self.client.post(url, {'image': ntf}, format='multipart')

        author.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('image', response.data)
        self.assertTrue(os.path.exists(author.image.path))

    def test_upload_image_bad_request(self):
        author = sample_author()
        url = image_upload_url(author.id)
        res = self.client.post(url, {'image': 'testnotimage'}, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
