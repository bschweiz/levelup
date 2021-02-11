# view module for handling 'game type' requests
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from levelupapi.models import GameType

class GameTypes(ViewSet):
    def retrieve( self, request, pk = None ):
        # handle GET requests for single game-Type
        try: 
            game_type = GameType.objects.get( pk = pk )
            serializer = GameTypeSerializer(game_type, context={ 'request': request })
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    

    def list(self, request):
        # handle GET requests for all game-Types
        gametypes = GameType.objects.all()
        # note: 'many=True', use for serializing an obj LIST rather than SINGLE obj
        serializer = GameTypeSerializer(
            gametypes, many=True, context={'request': request})
        return Response(serializer.data)

# here is the serializer, this class takes one arugment: serializers
class GameTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameType
        fields = ('id', 'label')
