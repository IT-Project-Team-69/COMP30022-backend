from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
import json


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
