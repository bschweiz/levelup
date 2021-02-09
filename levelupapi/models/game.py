from django.db import models
from .gamer import Gamer
from .gametype import GameType

class Game(models.Model):

    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    game_type = models.ForeignKey("GameType", on_delete= models.CASCADE)
    title = models.CharField(max_length=75)
    description = models.CharField(max_length=333)
    number_of_players = models.IntegerField()