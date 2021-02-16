from django.db import models
from .gamer import Gamer
from .game import Game

class Event(models.Model):

    scheduler = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    game = models.ForeignKey("Game", on_delete=models.CASCADE)
    event_time = models.DateTimeField(auto_now=False)
    location = models.CharField(max_length=50)

    @property
    def joined(self):
        return self.__joined
    
    @joined.setter
    def joined(self, value):
        self.__joined = value