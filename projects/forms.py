from django import forms

from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'status',
                  'github_url', 'participants')

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
