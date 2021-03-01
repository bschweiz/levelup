import json
from rest_framework import status
from rest_framework.test import APITestCase
from levelupapi.models import GameType

class GameTests(APITestCase):
    def setUp(self):
        #create new account and sample category
        url = '/register'
        data = {
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

        #seed the DB wit one game type so it don't break and there's no URL endpoint for creating GTs
        gametype = GameType()
        gametype.label = 'Stupid Type'
        gametype.save()

    def test_create_game(self):
        #verify we can create a game 
        # DEFINE GAME PROPERTIES
        url = '/games'
        data = {
            'gamer_id': 1,
            'gameTypeId': 1,
            'title': 'Clue',
            'description': 'Milton Bradley',
            'numberOfPlayers': 6,
        }
        #make sure the request is AUTHENTICATED
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        #initiate request and store response
        damn_response =self.client.post(url, data, format='json')
        #parse that shit into JSON
        json_response = json.loads(damn_response.content)
        #assert that the game was created
        self.assertEqual(damn_response.status_code, status.HTTP_201_CREATED)
        #assert that the properties on the damn resource are correct
        self.assertEqual(json_response['title'], 'Clue')
        self.assertEqual(json_response['description'], 'Milton Bradley')
        self.assertEqual(json_response['number_of_players'], 6)