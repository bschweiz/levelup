from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from levelupapi.models import Game, Event, Gamer
from levelupapi.views.game import GameSerializer

class Events(ViewSet):
    def create(self, request):
        #handle POST operations for events, returns serialized JSON instance
        scheduler = Gamer.objects.get(user = request.auth.user)
        game = Game.objects.get(pk = request.data["game_id"])
        # should the above 'game_id' be switched to camel case?
        event = Event()
        event.event_time = request.data["event_time"]
        event.location = request.data["location"]
        event.scheduler = scheduler
        event.game = game
        event.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk = None):
        # handles Delete request, response is 200, 404, or 500
        try:
            event = Event.objects.get(pk=pk)
            event.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Event.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def list(self, request):
    # handle GET all requests
    events = Event.objects.all()
    # support filtering by game
    game = self.request.query_params.get('game_id', None)
    if game is not None:
        events = events.filter(game__id=game)

        serializer = EventSerializer(
            events, many=True, context={'request': request})
        return Response(serializer.data)