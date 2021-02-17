from levelupapi.views.game import GameSerializer
from levelupapi.views.event import EventSerializer
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from levelupapi.models import Event, Gamer, Game

class Profiles(ViewSet):
    # handle GET request to profile resource, returns JSON of User info and events
    def list(self, request):
        gamer = Gamer.objects.get(user=request.auth.user)
        events = Event.objects.filter(eventgamer__gamer=gamer)

        events = EventSerializer(
            events, many=True, context={'request': request})
        gamer = GamerSerializer(
            gamer, many=False, context={'request': request})
        # there is NO MODEL for Profile so we gotta make an obj fr. scatch
        profile = {}
        profile['gamer'] = gamer.data
        profile['events'] = events.data

        return Response(profile)

class UserSerializer(serializers.ModelSerializer):
    # JSON serializer for gamer's related DJANGO 'User'
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')

class GamerSerializer(serializers.ModelSerializer):
    # JSON serilizer for gamers
    user = UserSerializer(many=False)

    class Meta:
        model = Gamer
        fields = ('user', 'bio')

class GameSerializer(serializers.ModelSerializer):
    # JSON serializer for games, not sure why exactly we are declaring it since not used yet as of chapter 13
    class Meta:
        model = Game
        fields = ('title', )

class EventSerializer(serializers.ModelSerializer):
    """JSON serializer for events"""
    game = GameSerializer(many=False)

    class Meta:
        model = Event
        fields = ('id', 'game', 'location', 'event_time')