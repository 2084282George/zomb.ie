from django.conf.urls import patterns, url
from zombieapp import views

urlpatterns = patterns('',
    url(r'^game/', views.game, name='game'),
    )
