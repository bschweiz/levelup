# view model for handling EVENT requests
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from levelupapi.models import Game, Event, Gamer, EventGamer
from levelupapi.views.game import GameSerializer


class Events(ViewSet):
    def create(self, request):
        # handle POST operations for events, returns serialized JSON instance
        event = Event()
        scheduler = Gamer.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data["gameId"])
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

    def retrieve(self, request, pk=None):
        # handle GET request for single event
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        # handles PUT requests, response should be a 204
        scheduler = Gamer.objects.get(user=request.auth.user)
        event = Event.object.get(pk=pk)
        game = Game.objects.get(pk=request.data["gameId"])

        event.event_time = request.data["eventTime"]
        event.location = request.data["location"]
        event.scheduler = scheduler
        event.game = game
        event.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
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
        # support filtering by game, ???? in ch10 i don't think i'm hiting this endpoint yet to know if i need to change it to camel case?
        # i don't think that there is an appropriant fetch function in EventProvider to hit this yet and ENABLE filtering events BY GAME
        game = self.request.query_params.get('game_id', None)
        if game is not None:
            events = events.filter(game__id=game)

        serializer = EventSerializer(
            events, many=True, context={'request': request})
        return Response(serializer.data)



    @action(methods=['post', 'delete'], detail=True)
    def signup(self, request, pk=None):
        # manages gamers signing up for events
        if request.method == "POST":
            # pk is the parameter of the query request before the verb
            event = Event.objects.get(pk=pk)
            # uses django 'authorixation' header to find which user is making the request to sign up
            gamer = Gamer.objects.get(user=request.auth.user)

            try:
                # check if they are already signed up
                registration = EventGamer.objects.get(
                    event=event, gamer=gamer)
                return Response(
                    {'message': 'Gamer already signed up for this event.'},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
            except EventGamer.DoesNotExist:
                registration = EventGamer()
                registration.event = event
                registration.gamer = gamer
                registration.save()

                return Response({}, status=status.HTTP_201_CREATED)

        # User wants to leave a previously joined event
        elif request.method == "DELETE":
            # if the game don't exist
            try:
                event = Event.objects.get(pk=pk)
            except Event.DoesNotExist:
                return Response(
                    {'message': 'Event does not exist.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # Get the authenticated user
            gamer = Gamer.objects.get(user=request.auth.user)

            try:
                # Try to delete the signup
                registration = EventGamer.objects.get(
                    event=event, gamer=gamer)
                registration.delete()
                return Response(None, status=status.HTTP_204_NO_CONTENT)

            except EventGamers.DoesNotExist:
                return Response(
                    {'message': 'Not currently registered for event.'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        return Response({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


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