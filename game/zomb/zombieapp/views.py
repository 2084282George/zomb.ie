from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from zombieapp.engine.game import Game
from zombieapp.engine.main import *
from zombieapp.models import Player
import django, dill

def home(request):
    return HttpResponseRedirect("/login/")

def logout(request):
    django.contrib.auth.logout(request)
    return HttpResponseRedirect("/login/")

def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/profile/")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = django.contrib.auth.authenticate(username=username, password=password)
        if user and user.is_active:
                django.contrib.auth.login(request, user)
                return HttpResponseRedirect("/profile/")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied. <a href='/login/'>Return</a>")
    else:
        return render(request, 'zombieapp/login.html', {"user": request.user})

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        picture = request.POST.get('picture')
        if True:
            user = django.contrib.auth.models.User()
            user.username = username
            user.set_password(password)
            player = Player()
            player.user = user
            if "picture" in request.FILES:
                player.picture = request.FILES["picture"]
            player.save()
            user.save()
    return render(request, 'zombieapp/register.html', {"user": request.user})

def leaderboard(request):

    return render(request, "zombieapp/leaderboard.html", {
        "user": request.user,
    })

def profile(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")
    return render(request, "zombieapp/profile.html", {
        "user": request.user,
        "statistics": dill.loads(Player.objects.get(user=request.user).statistics),
        "badges": dill.loads(Player.objects.get(user=request.user).badges),
        "player": Player.objects.get(user=request.user),
    })

def game(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")

    player = Player.objects.get(user=request.user)
    g = Game()

    def save():
        player.game = dill.dumps(g)
        player.save()

    move = None
    pos = None

    if request.POST:
        move = request.POST.get('move')
        pos = request.POST.get('pos')

    try:
        g = dill.loads(player.game)
    except:
        pass

    if not g.game_state:
        g.start_new_day()

    if move in g.turn_options():
        if move in ['MOVE','SEARCH'] and pos:
            g.take_turn(move, int(pos))
        else:
            g.take_turn(move)

    over = False
    party = 0
    if g.player_state.party > party:
        party = g.player_state.party

    if g.is_game_over():
        over = True

    if g.is_day_over():
        g.end_day()
        if g.is_game_over():
            over = True
        else:
            g.start_new_day()

    if over:
        player.statistics = dill.loads(player.statistics)
        player.badges = dill.loads(player.badges)

        if party > player.statistics['party']:
            player.statistics['party'] = party
        if player.statistics['best_days'] < g.player_state.days:
            player.statistics['best_days'] = g.player_state.days
        player.statistics['avg_days'] = \
            (player.statistics['avg_days'] * player.statistics['games'] + g.player_state.days) / (player.statistics['games'] + 1)
        player.statistics['avg_kills'] = \
            (player.statistics['avg_kills'] * player.statistics['games'] + g.player_state.kills) / (player.statistics['games'] + 1)
        if player.statistics['best_kills'] < g.player_state.kills:
            player.statistics['best_kills'] = g.player_state.kills
        player.statistics['games'] += 1

        if player.statistics['games'] == 5:
            player.badges += 'Games played (Bronze)'
        if player.statistics['games'] == 10:
            player.badges += 'Games played (Silver)'
        if player.statistics['games'] == 20:
            player.badges += 'Games played (Gold)'

        if player.statistics['best_kills'] == 10:
            player.badges += 'Zombies killed (Bronze)'
        if player.statistics['best_kills'] == 20:
            player.badges += 'Zombies killed (Silver)'
        if player.statistics['best_kills'] == 50:
            player.badges += 'Zombies killed (Gold)'

        if player.statistics['best_days'] == 5:
            player.badges += 'Days survived (Bronze)'
        if player.statistics['best_days'] == 10:
            player.badges += 'Days survived (Silver)'
        if player.statistics['best_days'] == 20:
            player.badges += 'Days survived (Gold)'

        if player.statistics['party'] == 10:
            player.badges += 'Party size (Bronze)'
        if player.statistics['party'] == 20:
            player.badges += 'Party size (Silver)'
        if player.statistics['party'] == 30:
            player.badges += 'Party size (Gold)'

        player.statistics = dill.dumps(player.statistics)
        player.badges = dill.dumps(player.badges)

        g = Game()
        save()
        return render(request, "zombieapp/game.html",
            {"message": "Aaarrrgh: You are dead! Game Over!", "user": request.user, "options": []})

    save()
    return render(request, "zombieapp/game.html",
        {"message": show_game_screen(g) + turn_options(g), "user": request.user, "options": g.turn_options})