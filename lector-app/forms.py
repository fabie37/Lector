from django import forms
from django.contrib.auth.models import User
import importlib
lector_app = importlib.import_module("lector-app.models")
from lector_app import UserProfile 

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = UserForm
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfileForm
        fields = ()