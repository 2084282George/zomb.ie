from django.conf.urls import patterns, url
from zombieapp import views

urlpatterns = patterns('',
    url(r'^game/', views.game, name='game'),
    url(r'^game_instructions/', views.game_instructions, name='Game instructions'),
    url(r'^leaderboard/', views.leaderboard, name='leaderboard'),
    url(r'^register/', views.register, name='register'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^login/', views.login, name='login'),
    )
