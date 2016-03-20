from django import forms
from django.contrib.auth.models import User
from zombieapp.models import Player

class UserForm(forms.ModelForm):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ('picture',)