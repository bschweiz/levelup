# view model for handling EVENT requests
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
        event = Event()
        scheduler = Gamer.objects.get(user = request.auth.user)
        game = Game.objects.get(pk = request.data["gameId"])
        event.event_time = request.data["eventTime"]
        event.location = request.data["location"]
        event.scheduler = scheduler
        event.game = game

        try:
            event.save()
            serializer = EventSerializer(event, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk = None):
        # handle GET request for single event
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk = None):
        # handles PUT requests, response should be a 204
        scheduler = Gamer.objects.get(user=request.auth.user)
        event = Event.object.get(pk=pk)
        game = Game.objects.get(pk = request.data["gameId"])

        event.event_time = request.data["eventTime"]
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

# using ModelSerializer to define our serializers for this ViewSet
class EventUserSerializer(serializers.ModelSerializer):
    # JSON serializer for event organizer's related Django user
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class EventGamerSerializer(serializers.ModelSerializer):
    # JSON serializer for scheduler
    user = EventUserSerializer(many=False)

    class Meta:
        model = Gamer
        fields = ['user']

class GameSerializer(serializers.ModelSerializer):
    # JSON serializer for games
    class Meta:
        model = Game
        fields = ('id', 'title', 'gamer_id', 'number_of_players')

class EventSerializer(serializers.ModelSerializer):
    # JSON serializer for events 
    scheduler = EventGamerSerializer(many=False)
    game = GameSerializer(many=False)

    class Meta:
        model = Event
        fields = ('id', 'scheduler', 'game', 
                    'event_time', 'location')

