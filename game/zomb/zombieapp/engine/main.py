__author__ = 'leif'

import os
from game import Game
from streetfactory import StreetFactory
from game import PlayerState



def main():

    # this is the basic game process
    # while the day or game is not over,
    # display the current state of the game,
    # then check what the player wants to do

    g = Game()
    while not g.is_game_over():
        #kick off the day
        g.start_new_day()
        while not g.is_day_over() and not g.is_game_over():
            os.system("clear")
            context_dict = {"gameState":g}
            show_game_screen(g)

            turn_options(g)

        # end the day
        g.end_day()


    print "Aaarrrgh: You are dead! Game Over!"




def show_game_screen(g):
    d = {}
    d = show_update_template(g)

    if g.game_state == 'STREET':
        d.update(show_street_template(g))
    if g.game_state == 'HOUSE':
        d.update(show_house_template(g))
    if g.game_state == 'ZOMBIE':
        d.update(show_zombie_template(g))
    return d


def turn_options(g):

    if turn in ['MOVE','SEARCH']:
        pos = int(raw_input('where (enter number of house/room): '))
        g.take_turn(turn, pos)
    else:
        g.take_turn(turn)


def show_street_template(g):
    d = {}
    print g.street
    i = 0
    for house in g.street.house_list:
        d["house{0}".format(i)] = house
        i += 1
    d[current_house] = g.street.get_current_house()
    return d

def show_house_template(g):
    d = {}
    d[current_house] = g.street.get_current_house()
    d[current_room] = g.street.get_current_house().get_current_room()
    return d

def show_zombie_template(g):
    d = {}
    current_room = g.street.get_current_house().get_current_room()
    d["zombies"]  = current_room.zombies
    return d


def show_update_template(g):
    d = {}
    if g.update_state.party!=0:
        d["party_inc"] = g.update_state.party


    if g.update_state.ammo != 0:
        d["ammo_inc"] = g.update_state.ammo

    if g.update_state.food != 0:
        d["food_inc2"] = g.update_state.food


    if g.update_state.kills > 0:
        d["kill_inc"] = g.update_state.kills

    if g.update_state.days > 0:
        d["day_inc"] = g.update_state.days
    return d

if __name__ ==  "__main__":
    main()
