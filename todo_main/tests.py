from django.test import TestCase
from django.http import Http404
from rest_framework.test import APIClient
from rest_framework import status
from . import serializer, views, models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Create your tests here.


class TestUserSerializer(TestCase):
    def setUp(self):
        self.validated_data = {"username": "hello", "password": "hello123"}
        self.serializer = serializer.UserSerializer()

    def test_create(self):
        user = self.serializer.create(self.validated_data)
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, self.validated_data["username"])
        self.assertTrue(user.check_password(self.validated_data["password"]))


class TestUserView(TestCase):
    def setUp(self):
        self.view = views.UserRegisteration.as_view()
        self.user_data = {"username": "hello", "password": "hello123"}
        self.err_user_data = {"username": "hello", "pass": "hello123"}

    def test_post(self):
        response = self.client.post(
            "/todo/register/", data=self.user_data, format="json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("data", response.data)
        self.assertIn("token", response.data)
        user = User.objects.get(username=self.user_data["username"])
        token = Token.objects.get(user=user)
        self.assertEqual(response.data["data"], serializer.UserSerializer(user).data)
        self.assertEqual(response.data["token"], str(token))

    def test_400post(self):
        response = self.client.post(
            "/todo/register/", data=self.err_user_data, format="json"
        )
        self.assertEqual(response.status_code, 400)


class TodoListTestCase(TestCase):
    def setUp(self):
        # creating user for Token
        self.user_data = {"username": "hello", "password": "hello123"}

        # create some test data
        self.err_data = {
            "title": "POST TEST CASE",
            "description": "Create a POST TEST CASE",
            "due_date": "2023-12-31",
            "status": "WORKEDD",  # err data
            "tags" : "Study Research",
        }
        self.data = {
            "title": "POST TEST CASE",
            "description": "Create a POST TEST CASE",
            "due_date": "2023-12-31",
            "status": "WORKING",
            "tags" : "Study Research",
        }
        models.todo.objects.create(
            title="Test1",
            description="Create a Test case",
            due_date="2023-12-31",
            status="OPEN",
            tags="test demo",
        )

    def get_token(self):
        self.client.post("/todo/register/", data=self.user_data, format="json")
        # get token obj
        tuser = User.objects.get(username=self.user_data["username"])
        return Token.objects.get(user=tuser)

    def test_get_todo_list(self):
        token = self.get_token()
        # create a client with the token
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=str("Token " + str(token)))
        # get the response from the view
        response = client.get("/todo/")
        # get the data from the db
        todos = models.todo.objects.all()
        serial = serializer.TodoSerializer(todos, many=True)
        # compare the two
        self.assertEqual(response.data, serial.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_todo_list(self):
        token = self.get_token()
        # create a client with the token
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=str("Token " + str(token)))
        # get the API response
        response = client.post("/todo/", self.data)
        # get the data from the db
        todo = models.todo.objects.get(title="POST TEST CASE")
        serial = serializer.TodoSerializer(todo)
        # compare the two
        self.assertEqual(response.data, serial.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_400post_todo(self):
        token = self.get_token()
        # create a client with the token
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=str("Token " + str(token)))
        # get the API response
        response = client.post("/todo/", self.err_data)
        # get the data from the db
        self.assertEqual(response.status_code, 400)


class TodoTodoDetailTestCases(TestCase):
    def setUp(self):
        # created a todo
        self.test1 = models.todo.objects.create(
            title="Test1",
            description="Create a Test case",
            due_date="2023-12-31",
            status="WORKING",
            tags= "test",
        )

        # creating user for Token
        self.user_data = {"username": "hello", "password": "hello123"}

        token = self.get_token()
        # create a client with the token
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=str("Token " + str(token)))

    def get_token(self):
        self.client.post("/todo/register/", data=self.user_data, format="json")
        # get token obj
        tuser = User.objects.get(username=self.user_data["username"])
        return Token.objects.get(user=tuser)

    def test_get_object(self):
        self.res = views.TodoDetail.get_object(self, pk=self.test1.pk)
        self.assertEqual(self.res, self.test1)
        # For error check
        with self.assertRaises(Http404):
            views.TodoDetail.get_object(self, pk=99)

    def test_get(self):
        self.test1.refresh_from_db()
        res = self.client.get(f"/todo/{self.test1.pk}/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update(self):
        updated_data = {
            "title": "Test1_2",
            "description": "Create a Test case",
            "due_date": "2024-01-01",
            "status": "DONE",
            "tags":["test"],
        }
        response = self.client.put(
            f"/todo/{self.test1.id}/", updated_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.test1.refresh_from_db()
        self.assertEqual(self.test1.title, updated_data["title"])
        self.assertEqual(self.test1.description, updated_data["description"])

        updated_err_data = {
            "topic": "Test1_2",
            "description": "Create a Test case",
            "due_date": "2024-01-01",
            "status": "DONE",
            "tags":["test"],
        }
        response2 = self.client.put(
            f"/todo/{self.test1.id}/", updated_err_data, format="json"
        )
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete(self):
        response = self.client.delete(f"/todo/{self.test1.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(models.todo.DoesNotExist):
            self.test1.refresh_from_db()
