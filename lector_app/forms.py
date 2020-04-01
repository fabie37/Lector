from django import forms
from . import models


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = models.User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = models.ListenerProfile
        fields = ()


class RecordingForm(forms.ModelForm):
    class Meta:
        model = models.Recording
        fields = ('book', 'reader','mp3file' )# SOS +duration