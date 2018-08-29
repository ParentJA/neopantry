# Standard library imports.
from io import BytesIO

# Django imports.
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

# Third-party imports.
from PIL import Image
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

__author__ = 'Jason Parent'

USERNAME = 'test.user@example.com'
PASSWORD = 'pAssw0rd!'


def create_user(username=USERNAME, password=PASSWORD):
    return get_user_model().objects.create_user(username=username, password=password)


def create_photo_file():
    data = BytesIO()
    Image.new('RGB', (100, 100)).save(data, 'PNG')
    data.seek(0)
    return SimpleUploadedFile('photo.png', data.getvalue())


class AuthenticationTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_can_sign_up(self):
        photo_file = create_photo_file()
        response = self.client.post(reverse('sign-up'), data={
            'username': USERNAME,
            'first_name': 'Test',
            'last_name': 'User',
            'password1': PASSWORD,
            'password2': PASSWORD,
            'photo': photo_file,
        })
        user = get_user_model().objects.last()
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(user.pk, response.data['id'])

    def test_user_can_log_in(self):
        user = create_user()
        response = self.client.post(reverse('log-in'), data={
            'username': user.username,
            'password': PASSWORD,
        })
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data['username'], user.username)

    def test_user_can_log_out(self):
        user = create_user()
        self.client.login(username=user.username, password=PASSWORD)
        response = self.client.delete(reverse('log-out'))
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)