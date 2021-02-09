# view model for handling GAME requests
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from levelupapi.models import Game, GameType, Gamer

class Games(ViewSet):
        # handle POST operations, returns JSON serialized GAME INSTANCE
    def create(self, request):
        # use token passed in the 'Authorization' header
        gamer = Gamer.objects.get(user = request.auth.user)
        # create a new Python instance of the Game class con properties de REQUEST de client 
        game = Game()
        game.title = request.data["title"]
        game.game_type_id = request.data["game_type_id"]
        game.number_of_players = request.data["number_of_players"]
        # game.skill_level = request.data["skillLevel"]
        game.gamer = gamer
        # now use the Djanog ORM to fetch the record from the database whose 'id' is what the client passed as game_type_id
        game_type = GameType.objects.get(pk=request.data["game_type_id"])
        game.game_type = game_type

        # try to save the new game to the db, then serialize it to JSON, then send that JSON back to client
        try:
            game.save()
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk = None):
    #handle GET request for single game, returns JSON serialized GAME INSTANCE
        try:
            # 'pk' is a parameter for this function, Django parses it from the URL, ie games/2, pk=2
            game = Game.objects.get(pk=pk)
            serializer = GameSerializer(game, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def update(self, request, pk = None):
        # handle PUT request for games, response: empty body with 204 status code
        gamer = Gamer.objects.get(user=request.auth.user)
        # get the game record w/ primary key equal to pk
        game = Game.objects.get (pk=pk)
        game.title = request.data["title"]
        game.game_type_id = request.data["game_type_id"]
        game.number_of_players = request.data["number_of_players"]
        # game.skill_level = request.data["skillLevel"]
        game.gamer = gamer
        game_type = GameType.objects.get(pk=request.data["game_type_id"])
        game.game_type = game_type
        game.save()
        # 204 status send back
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        #Handle DELETE requests/ single game, returns 200, 404, or 500 status code
        try:
            game = Game.objects.get(pk=pk)
            game.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Game.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        # handle GET all games, returns JSON serialized list of games
        games = Game.objects.all()
        # ORM command to get all game records from db
        game_type = self.request.query_params.get('type', None)
        # we can check to filter the games by type in a query string ie: games?type=1 would return all board games
        if game_type is not None:
            games = games.filter(game_type__id=game_type)
        serializer = GameSerializer(
            games, many=True, context={'request': request})
        return Response(serializer.data)


# JSON serializer for games, argument: serializer type
class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id','title', 'game_type_id', 'number_of_players','gamer_id')
        depth = 1
