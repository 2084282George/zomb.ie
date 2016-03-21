import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zomb.settings')

import django, dill
django.setup()

from zombieapp.models import Player

def populate():

    def create(name, add_more):
        user = django.contrib.auth.models.User()
        user.username = name
        user.set_password(name)
        user.save()
        player = Player()
        player.user = user
        if add_more:
            player.statistics = dill.dumps(
                {"games": 1, "best_days": 4, "avg_days": 4.0, "best_kills": 35, "avg_kills": 13.0, "party": 11}
            )
        player.save()

    create('jill', False)
    create('jim', True)
    create('joe', False)

if __name__ == '__main__':
    print "Starting Zombieapp population script..."
    populate()