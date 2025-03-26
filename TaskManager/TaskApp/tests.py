from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Task
from rest_framework.authtoken.models import Token

User = get_user_model()


class TaskManagementAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='securepassword')
        self.user2 = User.objects.create_user(username='testuser2', email='test2@example.com', password='securepassword')
        self.token, _ = Token.objects.get_or_create(user=self.user)

        self.client.login(username='testuser', password='securepassword')
        # self.token = self.client.post('/task/api/token/', {'username': 'testuser', 'password': 'securepassword'}).data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token))

    def test_user_registration(self):
        response = self.client.post('/task/api/register/', {
            "username": "newuser",
            "email": "new@example.com",
            "password": "securepassword",
            "mobile": "1234567890"
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)

        user_exists = User.objects.filter(username="newuser").exists()
        self.assertTrue(user_exists)

    def test_obtain_auth_token(self):
        response = self.client.post('/task/api/api-token-auth/', {
            "username": "testuser",
            "password": "securepassword"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_create_task(self):
        response = self.client.post('/task/api/tasks/', {
            "name": "Test Task",
            "description": "Test task description",
            "task_type": "development",
            "status": "pending"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Test Task")

    def test_assign_task_to_users(self):
        task = Task.objects.create(name="Assign Test Task", description="Test", status="pending")
        response = self.client.post(f'/task/api/tasks/{task.id}/assign/', {
            "user_ids": [self.user.id, self.user2.id]
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(task.assigned_users.count(), 2)

    def test_retrieve_tasks_for_user(self):
        task = Task.objects.create(name="Retrieve Test Task", description="Test", status="pending")
        task.assigned_users.add(self.user)
        response = self.client.get('/task/api/tasks/my_tasks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
