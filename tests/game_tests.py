import json
from rest_framework import status
from rest_framework.test import APITestCase
from levelupai.models import GameType

class GameTests(APITestCase):
    def setUp(self):
        #create new account and sample category
        url = '/register'
        data = = {
            'username': 'steve',
            'password': 'Admin8*',
            'email': 'steve@stevebrownlee.com',
            'address': '100 Infinity Way',
            'phone_number': '555-1212',
            'first_name': 'Steve',
            'last_name': 'Brownlee',
            'bio': 'Love those gamez!!'
        }