from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse


class SignUpTest(TestCase):
    def test_create_user_account(self):
        url = reverse('useraccounts')
        
