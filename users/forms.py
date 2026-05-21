from django import forms
from django.contrib.auth.forms import \
    AuthenticationForm as BaseAuthenticationForm
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm

from .models import User


class UserCreateForm(BaseUserCreationForm):
    class Meta(BaseUserCreationForm.Meta):
        model = User
        fields = ('email', 'name', 'surname')


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'surname', 'phone', 'github_url', 'about')

    def clean_github_url(self):
        url = self.cleaned_data.get('github_url')
        if not url:
            return url
        domain = url.split('://')[1][:10]
        if domain != 'github.com':
            raise forms.ValidationError(
                "Ссылка должна вести на официальный сайт GitHub"
            )
        return url


class LoginForm(BaseAuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
        label='Email'
    )
