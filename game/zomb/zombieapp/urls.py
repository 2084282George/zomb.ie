from django.conf.urls import patterns, url
from zombieapp import views

urlpatterns = patterns('',
<<<<<<< HEAD
    url(r'^game/', views.game, name='game'),
    url(r'^game_instructions/', views.game_instructions, name='Game instructions'),
    url(r'^leaderboard/', views.leaderboard, name='leaderboard'),
    url(r'^register/', views.register, name='register'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^login/', views.login, name='login'),
    )
=======
    url(r'^$', views.home, name='home'),
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^leaderboard/$', views.leaderboard, name='leaderboard'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^game/$', views.game, name='game'),
    url(r'^logout/$', views.logout, name='logout')
)
>>>>>>> 716d89f7baad635312d03ee2c2910872989e8d2a
