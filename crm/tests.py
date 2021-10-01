from django.test import TestCase
from rest_framework import status
from django.contrib.auth.models import User


class SignUpTest(TestCase):
    def setUp(self):
        self.url = '/crm/useraccounts/'
        self.userData = {'username': 'test_user@gmail.com',
                         'password': 'Today12345',
                         'first_name': 'Test',
                         'last_name': 'User'}

    def test_create_user_account(self):
        '''
        Ensure user can create a new account
        '''
        response = self.client.post(self.url, self.userData, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], self.userData['username'])
        self.assertEqual(response.data['email'], self.userData['username'])
        self.assertEqual(response.data['first_name'],
                         self.userData['first_name'])
        self.assertEqual(response.data['last_name'],
                         self.userData['last_name'])
        self.assertEqual(response.data['is_superuser'], False)

    def test_create_account_fail_username_taken(self):
        '''
        Ensure user accounts cannot have the same username
        '''
        user = User.objects.create(
            username=self.userData['username'], password=self.userData['password'])
        user.save()
        response = self.client.post(self.url, self.userData, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LogInTest(TestCase):
    def setUp(self):
        self.url = '/crm/api-auth/alt-login/'
        self.logInData = {'username': 'test_user@gmail.com',
                          'password': 'Today12345'}
        user = User.objects.create_user(
            username=self.logInData['username'], password=self.logInData['password'])
        user.save()

    def test_login_success(self):
        '''
        Ensure users can log in with correct username and password
        '''
        response = self.client.post(
            self.url, self.logInData, format="json", content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.json()
        self.assertEqual(response['success'], True)

    def test_login_fail_incorrect_password(self):
        '''
        Ensure users cannot log in with the incorrect password
        '''
        data = {
            'username': self.logInData['username'],
            'password': 'IncorrectPassword'
        }
        response = self.client.post(
            self.url, data, format="json", content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.json()
        self.assertEqual(response['success'], False)


class EnterEmailTest(TestCase):
    def setUp(self):
        self.url = '/crm/api-auth/checkemail/'
        self.user = User.objects.create_user(
            username="test@gmail.com", password="Today12345")
        self.user.save()

    def test_enter_existing_email(self):
        '''
        Ensures API returns true if email is associated with a user
        '''
        data = {
            "email": self.user.username
        }
        response = self.client.post(
            self.url, data, format="json", content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.json()
        self.assertEqual(response['success'], True)

    def test_enter_not_existing_email(self):
        '''
        Ensures API returns false if email is not associated with an existing user
        '''
        data = {
            "email": "some.email@gmail.com"
        }
        response = self.client.post(
            self.url, data, format="json", content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.json()
        self.assertEqual(response['success'], False)


class UserProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test@gmail.com",
            password="Today12345",
            first_name="Jane",
            last_name="Doe")
        self.user.save()
        self.url = f'/crm/userprofiles/{self.user.id}/'

    def test_get_user_details(self):
        '''
        Ensure user can view correct user details
        '''
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.user.id)
        self.assertEqual(response.data['organisation'], "")
        self.assertEqual(response.data['role'], "")
        self.assertEqual(response.data['phoneNumber'], "")
        self.assertEqual(response.data['image'], None)

    def test_update_user_details(self):
        '''
        Ensure user can update user details
        '''
        data = {
            "organisation": "The University of Melbourne",
            "role": "Computer Science Student"
        }
        response = self.client.patch(
            self.url, data, format="json", content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['organisation'], data['organisation'])
        self.assertEqual(response.data['role'], data['role'])

    def test_adding_custom_profile_fields(self):
        '''
        Ensures user can add custom fields and field values to their profile
        '''
        url = f"{self.url}fields/"
        data = {
            "fields": [
                {
                    "label": "Preferred Name",
                    "value": "Jane",
                    "userAccount": self.user.id
                },
                {
                    "label": "Pronouns",
                    "value": "She/Her",
                    "userAccount": self.user.id
                }
            ]
        }
        response = self.client.post(url, data, format="json", content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), len(data['fields']))
        
