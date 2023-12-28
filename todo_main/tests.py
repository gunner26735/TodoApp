from django.test import TestCase
from . import serializer,views
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Create your tests here.

class TestUserSerializer(TestCase):
    def setUp(self):
        self.validated_data = {
            'username': 'hello',
            'password': 'hello123'
        }
        self.serializer = serializer.UserSerializer()

    def test_create(self):
        user = self.serializer.create(self.validated_data)
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, self.validated_data['username'])
        self.assertTrue(user.check_password(self.validated_data['password']))


class TestUserView(TestCase):
    def setUp(self):
        self.view = views.UserRegisteration.as_view()
        self.user_data = {
            'username': 'hello',
            'password': 'hello123'
        }
        self.err_user_data = {
            'username': 'hello',
            'pass': 'hello123'
        }

    def test_post(self):
        response = self.client.post('/todo/register/',data=self.user_data,format='json')
        self.assertEqual(response.status_code,201)
        self.assertIn('data', response.data)
        self.assertIn('token', response.data)
        user = User.objects.get(username=self.user_data['username'])
        token = Token.objects.get(user=user)
        self.assertEqual(response.data['data'], serializer.UserSerializer(user).data)
        self.assertEqual(response.data['token'], str(token))

    def test_400post(self):
        response = self.client.post('/todo/register/',data=self.err_user_data,format='json')
        self.assertEqual(response.status_code,400)
