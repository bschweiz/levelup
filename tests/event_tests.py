import json
from rest_framework import status
from rest_framework.test import APITestCase
from levelupapi.models import Event, Game, GameType

class EventTests(APITestCase):
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
        gametype.label = 'Classic Type'
        gametype.save()
        #now make a dummy game and save it
        game = Game()
        game.game_type_id = 1
        game.title = 'Chess'
        game.description = 'GOAT Board Game'
        game.number_of_players = 2
        game.gamer_id = 1
        game.save()

    def test_create_evnt(self):
        #verify we can create an event 
        # DEFINE EVENT PROPERTIES
        url = '/events'
        data = {
            'scheduler': 1,
            'game_id': 1,
            'event_time': '2021-03-11T14:00:00.000Z',
            'location': 'NSS'
        }
        #make sure the request is AUTHENTICATED
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        #initiate request and store response
        this_response =self.client.post(url, data, format='json')
        #parse that shit into JSON
        json_response = json.loads(this_response.content)
        #assert that the game was created
        self.assertEqual(this_response.status_code, status.HTTP_201_CREATED)
        #assert that the properties on the this resource are correct
        self.assertEqual(json_response['event_time'], '2021-03-11T14:00:00.000Z')
        self.assertEqual(json_response['description'], 'Milton Bradley')
        self.assertEqual(json_response['number_of_players'], 6)

    def test_get_game(self):
        #check to see if we can get an existing game, 1st seed the DB
        game = Game()
        game.game_type_id = 1
        game.title = 'Chess'
        game.description = 'GOAT Board Game'
        game.number_of_players = 2
        game.gamer_id = 1
        game.save()
        #make sure request is authenticated
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        #initi8ate request and store response
        response = self.client.get(f'/games/{game.id}')
        #json rESPONSE JUST FUCKING PARSE IT!!!
        json_response = json.loads(response.content)
        #assert that the game WAS RETRIEVED SUCCESSFULLY
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #assert that the values are correct
        self.assertEqual(json_response['title'], 'Chess')
        self.assertEqual(json_response['description'], 'GOAT Board Game')
        self.assertEqual(json_response['number_of_players'], 2)

    def test_change_game(self):
        #test we can update an existing game
        game = Game()
        game.game_type_id = 1
        game.title = 'Chess'
        game.description = 'GOAT Board Game'
        game.number_of_players = 2
        game.gamer_id = 1
        game.save()
        #now define NEW properties for this shit
        data = {
            'gameTypeId': 1,
            'title': 'Clue',
            'description': 'Milton Bradley',
            'numberOfPlayers': 6,
        }

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(f'/games/{game.id}', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        #verify the changes
        response = self.client.get(f'/games/{game.id}')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #assert that the properties on the this resource are correct
        self.assertEqual(json_response['title'], 'Clue')
        self.assertEqual(json_response['description'], 'Milton Bradley')
        self.assertEqual(json_response['number_of_players'], 6)

    def test_delete_game(self):
        #make sure we can delete a game
        game = Game()
        game.game_type_id = 1
        game.title = 'Chess'
        game.description = 'GOAT Board Game'
        game.number_of_players = 2
        game.gamer_id = 1
        game.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(f'/games/{game.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # GET GAME AGAIN TO VERIFY 404 response
        response = self.client.get(f'/games/{game.id}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)