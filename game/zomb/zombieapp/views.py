from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from zombieapp.engine.game import Game
from zombieapp.engine.main import *
from zombieapp.models import Player, Guest
from zombieapp.forms import UserForm, PlayerForm
from django.contrib.auth.models import User
import django, dill

def home(request):
    return HttpResponseRedirect("/login/")

def logout(request):
    django.contrib.auth.logout(request)
    return HttpResponseRedirect("/login/")

def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/profile/"+request.user.username)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = django.contrib.auth.authenticate(username=username, password=password)
        if user and user.is_active:
            django.contrib.auth.login(request, user)
            return HttpResponseRedirect("/profile/"+request.user.username)
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

    for player in Player.objects.all():
        statistics = dill.loads(player.statistics)
        player.best_kills = statistics['best_kills']
        player.best_days = statistics['best_days']
        player.avg_kills = statistics['avg_kills']
        player.avg_days = statistics['avg_days']
        player.party = statistics['party']
        player.save()
    best_kills_leaderboard = Player.objects.order_by('-best_kills')[:20]
    best_days_leaderboard = Player.objects.order_by('-best_days')[:20]
    avg_days_leaderboard = Player.objects.order_by('-avg_days')[:20]
    avg_kills_leaderboard = Player.objects.order_by('-avg_kills')[:20]
    party_leaderboard = Player.objects.order_by('-party')[:20]
    return render(request, "zombieapp/leaderboard.html", {
        "user": request.user,"best_kills_leaderboard": best_kills_leaderboard,
        "best_days_leaderboard":best_days_leaderboard,
        "avg_days_leaderboard":avg_days_leaderboard,
        "avg_kills_leaderboard":avg_kills_leaderboard,
        "party_leaderboard":party_leaderboard
    })

def profile(request,profile_name):

    profBadges = 0
    user = 0
    statistics = 0
    badges = 0
    player = 0
    flag = True
    players = 0
    username = 0
    if request.user.is_authenticated():
        player = Player()
        try:
            player = Player.objects.get(user=request.user)
        except:
            player.user = request.user
            player.save()

        player.statistics = dill.loads(player.statistics)
        player.badges = dill.loads(player.badges)

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

        player.save()

        badges = dill.loads(player.badges)
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
        player.user = request.user
        if 'picture' in request.FILES:
            player.picture = request.FILES['picture']
        player.save()
        statistics=dill.loads(Player.objects.get(user=request.user).statistics)
        players = Player.objects.all()
        user = request.user
        username = user.username
    prof = 0
    profStatistics = 0
    profFlag = True
    if(User.objects.all().filter(username=profile_name).exists()):
        prof = User.objects.get(username=profile_name)
        if(Player.objects.all().filter(user=prof).exists()):
            prof = Player.objects.get(user=prof)
            profStatistics = dill.loads(prof.statistics)
            profBadges = dill.loads(prof.badges)
            if len(profBadges)==0:
                profFlag = False
    return render(request, "zombieapp/profile.html", {
        "user": user,
        "statistics": statistics,
        "badges": badges,
        "player": player,
        "flag": flag,
        "players": players,
        "prof":prof,
        "isProfile": profile_name == username,
        "profileExists": prof != 0,
        "profStatistics": profStatistics,
        "profFlag": profFlag,
        "profile_name": profile_name,
        "profBadges": profBadges
    })

def game(request):
    player = Guest()
    player.ip = dill.dumps(request.META.get("REMOTE_ADDR"))
    if request.user.is_authenticated():
        player = Player.objects.get(user=request.user)
    else:
        try:
            player = Guest.objects.get(ip=dill.dumps(request.META.get("REMOTE_ADDR")))
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
			try:
				g.take_turn(move, int(pos))
			except:
				pass
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

        player.statistics = dill.dumps(player.statistics)
        player.badges = dill.dumps(player.badges)

        g = Game()
        save()
        return render(request, "zombieapp/game.html",
            {"message": "Aaarrrgh: You are dead! Game Over!", "user": request.user, "options": []})

    save()

    if request.POST:
        if request.POST.get("restart") == "true":
            g = Game()
            save()
            return HttpResponseRedirect('/game/')
    return render(request, "zombieapp/game.html",
        {"message": show_game_screen(g) +
                    turn_options(g), "user": request.user, "options": g.turn_options})