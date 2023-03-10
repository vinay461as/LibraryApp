from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('create')
TOKEN_URL = reverse('token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class UserApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.payload = {
            'username': 'abc',
            'password': 'test123456'
        }

    def test_create_valid_user_success(self):
        response = self.client.post(CREATE_USER_URL, self.payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(self.payload['password']))
        self.assertNotIn('password', response.data)

    def test_user_exist(self):
        create_user(**self.payload)
        response = self.client.post(CREATE_USER_URL, self.payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        payload = self.payload.copy()
        payload['password'] = 'ab'
        response = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        user_exist = get_user_model().objects.filter(email=payload['username']).exists()
        self.assertFalse(user_exist)

    def test_create_token_for_user(self):
        payload = self.payload.copy()
        create_user(**payload)
        response = self.client.post(TOKEN_URL, {'username': 'abc', 'password': 'test123456'})
        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        create_user(username='abc', password='123')
        response = self.client.post(TOKEN_URL, {'username': 'abc', 'password': 'test123456'})
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        response = self.client.post(TOKEN_URL, {'username': 'abc', 'password': 'test123456'})
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        response = self.client.post(TOKEN_URL, {'username': 'check', 'password': ''})
        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
