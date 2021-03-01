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
        #initiate request and grab the response
        response = self.client.post(url, data, format='json')
        #parse the JSON in the resonse body
        fuckin_json_response = json.loads(response.content)
        #store teh AUTH Token
        self.token = fuckin_json_response['token']
        #assert that a user was created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
