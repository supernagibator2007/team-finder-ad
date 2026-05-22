from urllib.parse import urlsplit

from django import forms

from .models import Project
from utils.const import GITHUB_LINK


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'status',
                  'github_url', 'participants')

    def clean_github_url(self):
        url = self.cleaned_data.get('github_url')
        if not url:
            return url
        parsed_url = urlsplit(url)
        if parsed_url.hostname != GITHUB_LINK:
            raise forms.ValidationError(
                "Ссылка должна вести на официальный сайт GitHub"
            )
        return url
