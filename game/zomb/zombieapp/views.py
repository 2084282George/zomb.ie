from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from zombieapp.engine.game import Game
from zombieapp.engine.main import *
from zombieapp.models import Player, Guest
from zombieapp.forms import UserForm, PlayerForm
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
        user_form = UserForm(data=request.POST)
        player_form = PlayerForm(data=request.POST)
        if user_form.is_valid() and player_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            player = player_form.save(commit=False)
            player.user = user
            if 'picture' in request.FILES:
                player.picture = request.FILES['picture']
            player.save()
            return HttpResponseRedirect('/login/')
        else:
            print user_form.errors, player_form.errors
    else:
        user_form = UserForm()
        player_form = PlayerForm()
    return render(request, 'zombieapp/register.html', {'user_form': user_form, 'player_form': player_form, "user": request.user})

def instructions(request):
    return render(request, "zombieapp/instructions.html", {"user": request.user})

def leaderboard(request):

    return render(request, "zombieapp/leaderboard.html", {
        "user": request.user,
    })

def profile(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/login/")
    player = Player()
    try:
        player = Player.objects.get(user=request.user)
    except:
        player.user = request.user
        player.save()
    badges = dill.loads(player.badges)
    flag = True
    if len(badges) == 0:
        flag = False
    password = request.POST.get("password")
    if password:
        try:
            request.user.set_password(password)
            request.user.save()
            logout(request)
            return HttpResponseRedirect('/login/')
        except:
            return HttpResponse("Invalid password")
    if "picture" in request.FILES:
        player.picture = request.FILES["picture"]
        player.save()
    return render(request, "zombieapp/profile.html", {
        "user": request.user,
        "statistics": dill.loads(Player.objects.get(user=request.user).statistics),
        "badges": badges,
        "player": player,
        "flag": flag,
    })

def game(request):
    player = Guest()
    if request.user.is_authenticated():
        player = Player.objects.get(user=request.user)
    else:
        try:
            player = Guest.objects.get()
        except:
            pass

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

    player.statistics = dill.loads(player.statistics)
    if g.player_state.party > player.statistics['party']:
            player.statistics['party'] = g.player_state.party
    player.statistics = dill.dumps(player.statistics)

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
            player.badges += ['Games played (Bronze)']
        if player.statistics['games'] == 10:
            player.badges += ['Games played (Silver)']
        if player.statistics['games'] == 20:
            player.badges += ['Games played (Gold)']

        if player.statistics['best_kills'] >= 10 and 'Zombies killed (Bronze)' not in player.badges:
            player.badges += ['Zombies killed (Bronze)']
        if player.statistics['best_kills'] >= 20 and 'Zombies killed (Silver)' not in player.badges:
            player.badges += ['Zombies killed (Silver)']
        if player.statistics['best_kills'] >= 50 and 'Zombies killed (Gold)' not in player.badges:
            player.badges += ['Zombies killed (Gold)']

        if player.statistics['best_days'] >= 5 and 'Days survived (Bronze)' not in player.badges:
            player.badges += ['Days survived (Bronze)']
        if player.statistics['best_days'] >= 10 and 'Days survived (Silver)' not in player.badges:
            player.badges += ['Days survived (Silver)']
        if player.statistics['best_days'] >= 20 and 'Days survived (Gold)' not in player.badges:
            player.badges += ['Days survived (Gold)']

        if player.statistics['party'] >= 10 and 'Party size (Bronze)' not in player.badges:
            player.badges += ['Party size (Bronze)']
        if player.statistics['party'] >= 20 and 'Party size (Silver)' not in player.badges:
            player.badges += ['Party size (Silver)']
        if player.statistics['party'] >= 30 and 'Party size (Gold)' not in player.badges:
            player.badges += ['Party size (Gold)']

        player.statistics = dill.dumps(player.statistics)
        player.badges = dill.dumps(player.badges)

        g = Game()
        save()
        return render(request, "zombieapp/game.html",
            {"message": "Aaarrrgh: You are dead! Game Over!", "user": request.user, "options": []})

    save()
    return render(request, "zombieapp/game.html",
        {"message": show_game_screen(g) + turn_options(g), "user": request.user, "options": g.turn_options})