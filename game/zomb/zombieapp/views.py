import imp
from zombieapp.engine import main
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from zombieapp.engine.game import Game
from zombieapp.engine.streetfactory import StreetFactory
from zombieapp.engine.game import PlayerState



# Create your views here.

def game(request):

    context_dict={}
    # this is the basic game process
    # while the day or game is not over,
    # display the current state of the game,
    # then check what the player wants to do

    g = Game()
    context_dict["gameProg"] = g
    while not g.is_game_over():
        #kick off the day
        g.start_new_day()
        context_dict["gameProg"] = g
        while not g.is_day_over() and not g.is_game_over():
            show_game_screen_ajax(request, g)
            turn_options_ajax(request, g)
            main.turn_options(g)
            context_dict["gameProg"] = g

        # end the day
        g.end_day()
        context_dict["gameProg"] = g

    
    return render("game over!")
    
def do_action(action):
    g.take_turn(g, action)
    return g
    
    
def show_game_screen_ajax(request, g):
    d = main.show_game_screen(g)
    return HttpResponse("response from game")
    
def turn_options_ajax(request, g):
    d = main.turn_options(g)
