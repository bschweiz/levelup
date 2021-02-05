from django.db import models
from .gamer import Gamer
from .game import Games

class Event(models.Model):

    scheduler = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    game = models.ForeignKey("Games", on_delete=models.CASCADE)
    event_time = models.DateTimeField(auto_now=False)
    location = models.CharField(max_length=50)