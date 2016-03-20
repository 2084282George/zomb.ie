from django.conf.urls import patterns, url
from zombieapp import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^leaderboard/$', views.leaderboard, name='leaderboard'),
    url(r'^profile/(?P<profile_name>[\w@.+-_]+)/$', views.profile, name='profile'),
    url(r'^game/$', views.game, name='game'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^instructions/$', views.instructions, name='instructions'),
)
