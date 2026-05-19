import json
from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, UpdateView, ListView
from django.urls import reverse
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from .models import User, Skill
from .forms import CustomUserChangeForm


def skills_search(request):
    query = request.GET.get('q', '')
    if not query:
        return JsonResponse([])
    queryset = Skill.objects.filter(
        name__istartswith=query
    ).order_by('name').values('id', 'name')[:10]
    return JsonResponse(list(queryset), safe=False)


def add_skill(request, pk):
    if request.user.id != pk:
        return HttpResponseForbidden('У вас нет прав')
    data = json.loads(request.body)
    skill_id = data.get('skill_id')
    name = data.get('name', '')
    skill = None
    created = False
    added = False
    if skill_id:
        skill = Skill.objects.get(id=skill_id)
    elif name:
        skill, created = Skill.objects.get_or_create(
            name__iexact=name,
            defaults={'name': name}
        )
    if request.user.skills.filter(id=skill.id).exists():
        return JsonResponse({'error': 'Навык уже есть'}, status=400)
    request.user.skills.add(skill)
    added = True
    return JsonResponse({
        'skill_id': skill.id,
        'name': skill.name,
        'created': created,
        'added': added
    })


@login_required
def remove_skill(request, pk, skill_pk):
    if request.user.id != pk:
        return HttpResponseForbidden('У вас нет прав')
    skill = get_object_or_404(Skill, id=skill_pk)
    request.user.skills.remove(skill)
    return redirect('users:detail', pk=pk)


def logout_view(request):
    logout(request)
    return redirect('/')


class UserListView(ListView):
    model = User
    template_name = 'users/participants.html'
    context_object_name = 'participants'

    def get_queryset(self):
        queryset = super().get_queryset()
        skill_name = self.request.GET.get('skill')
        if skill_name:
            queryset = queryset.filter(skills__name__exact=skill_name)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_skill'] = self.request.GET.get('skill')
        context['all_skills'] = Skill.objects.all()
        return context


class UserDetailView(DetailView):
    model = User
    template_name = 'users/user-details.html'


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'users/edit_profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('users:detail', kwargs={'pk': self.request.user.pk})


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/change_password.html'

    def get_success_url(self):
        return reverse('users:detail', kwargs={'pk': self.request.user.pk})
