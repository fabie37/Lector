from django import forms

from . import models


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = models.User
        fields = ('first_name','last_name','email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = models.ListenerProfile
        fields = ()


class RecordingForm(forms.ModelForm):
    class Meta:
        model = models.Recording
        fields = ('book', 'mp3file' )# TODO +username +duration
