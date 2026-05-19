from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class CustomUserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'name', 'surname')


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'surname', 'phone', 'github_url', 'about')


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')
