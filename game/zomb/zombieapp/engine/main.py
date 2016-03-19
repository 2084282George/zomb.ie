__author__ = "leif"
from os import linesep
from zombieapp.engine.game import Game

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

        g.end_day()        # end the day
    print "Aaarrrgh: You are dead! Game Over!"

def show_game_screen(g):
    s = "------------------------------------------" + linesep
    s += "ZZZZZ   OOO    MM    MM  BBBB   III  EEEEE" + linesep
    s += "   Z   OO OO   MMM  MMM  B   B   I   E" + linesep
    s += "  Z   OO   OO  MM MM MM  BBBB    I   EEE" + linesep
    s += " Z     OO OO   MM    MM  B   B   I   E" + linesep
    s += "ZZZZZ   OOO    MM    MM  BBBBB  III  EEEEE" + linesep
    s += "------------------------------------------" + linesep
    s += "Player Status" + linesep
    s += "------------------------------------------" + linesep
    s += str(g.player_state) + 2*linesep
    s += "Day: {0}, Time left in day: {1}".format(g.player_state.days, g.time_left) + linesep
    s += "------------------------------------------" + linesep
    s += show_update_template(g)
    s += "------------------------------------------" + linesep
    if g.game_state == 'STREET':
        s += show_street_template(g)
    if g.game_state == 'HOUSE':
        s += show_house_template(g)
    if g.game_state == 'ZOMBIE':
        s += show_zombie_template(g)
    s += "------------------------------------------" + linesep
    return s

def turn_options(g):
    s = linesep + "Available options:" + str(g.turn_options()) + linesep
    s += "------------------------" + linesep
    return s + 'What do you want to do (enter full word i.e. MOVE, SEARCH, etc): '

def show_street_template(g):
    s = "You are in a Street!" + linesep
    s += str(g.street) + linesep
    i = 0
    for house in g.street.house_list:

        s += "House: " + str(i) + " " + str(house) + linesep

        i += 1
    s += linesep + "------------------------------------------" + linesep
    s += "You are out the front of:" + linesep
    s += str(g.street.get_current_house()) + linesep
    return s

def show_house_template(g):
    s = "You are in a house!" + linesep
    s += str(g.street.get_current_house()) + linesep
    s += str(g.street.get_current_house().get_current_room()) + linesep
    return s

def show_zombie_template(g):
    current_room = g.street.get_current_house().get_current_room()
    return "zaarrrr rrrgh: {0} Zombies!!!!".format(current_room.zombies) + linesep

def show_update_template(g):
    s = ""
    if g.update_state.party<0:
        s += "You lost: {0} people".format(abs(g.update_state.party)) + linesep

    if g.update_state.party>0:
        s += "{0} more people have joined your party".format(g.update_state.party) + linesep

    if g.update_state.ammo > 0:
        s += "You found: {0} units of ammo".format(g.update_state.ammo) + linesep

    if g.update_state.ammo < 0:
        s += "You used: {0} units of ammo".format(abs(g.update_state.ammo)) + linesep

    if g.update_state.food > 0:
        s += "You found: {0} units of food".format(g.update_state.food) + linesep

    if g.update_state.food < 0:
        s += "You used: {0} units of food".format(abs(g.update_state.food)) + linesep

    if g.update_state.kills > 0:
        s += "You killed: {0} zombies".format(g.update_state.kills) + linesep

    if g.update_state.days > 0:
        s += "New Day: You survived another day!" + linesep
    return s
