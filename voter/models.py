from django.db import models
import json


class Votes(models.Model):
    room_id = models.CharField(max_length=100)
    A = models.IntegerField(default=0)
    B = models.IntegerField(default=0)
    X = models.IntegerField(default=0)
    Y = models.IntegerField(default=0)

    def __str__(self):
        return "A: {}, B: {}, X: {}, Y: {}".format(self.A, self.B, self.X, self.Y)

