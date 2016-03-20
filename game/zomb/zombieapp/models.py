from django.db import models
from django.contrib.auth.models import User
from picklefield.fields import PickledObjectField
from zombieapp.engine.game import Game
import dill

class Player(models.Model):
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to='profile_pictures', blank=True)
    game = PickledObjectField(default=dill.dumps(Game()))
    badges = PickledObjectField(default=dill.dumps([]))
    statistics = PickledObjectField(default=dill.dumps(
        {"games": 0, "best_days": 0, "avg_days": 0.0, "best_kills": 0, "avg_kills": 0.0, "party": 0})
    )

    def __unicode__(self):
        return self.user.username

class Guest(models.Model):
    game = PickledObjectField(default=dill.dumps(Game()))
    badges = PickledObjectField(default=dill.dumps([]))
    statistics = PickledObjectField(default=dill.dumps(
        {"games": 0, "best_days": 0, "avg_days": 0.0, "best_kills": 0, "avg_kills": 0.0, "party": 0})
    )