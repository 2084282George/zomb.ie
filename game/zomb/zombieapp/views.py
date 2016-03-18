from zombieapp.engine import main
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from zombieapp.engine.game import Game
from zombieapp.engine.streetfactory import StreetFactory
from zombieapp.engine.game import PlayerState



# Create your views here.

g = Game()

def game(request):

    context_dict={}
    # this is the basic game process
    # while the day or game is not over,
    # display the current state of the game,
    # then check what the player wants to do

    global g
    context_dict["gameProg"] = g
    """while not g.is_game_over():
        #kick off the day
        g.start_new_day()
        context_dict["gameProg"] = g
        while not g.is_day_over() and not g.is_game_over():
            main.show_game_screen(g)
            main.turn_options(g)
            context_dict["gameProg"] = g

        # end the day
        g.end_day()
        context_dict["gameProg"] = g"""

    
    return render(request,'zombieapp/game.html')

def index(request):
    return render(request, 'zombieapp/index.html')

def login(request):
    return render(request,'zombieapp/login.html')

def register(request):
    return render(request,'zombieapp/register.html')

def game_instructions(request):
    return render(request,'zombieapp/game_instructions.html')

def profile(request):
    return render(request,'zombieapp/profile.html')

def leaderboard(request):
    return render(request, 'zombieapp/leaderboard.html')
    
def do_action(action):
    g.take_turn(g, action)
    return g

