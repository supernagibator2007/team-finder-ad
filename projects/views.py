from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from utils.const import PAGINATION, STATUS_CLOSED

from .forms import ProjectForm
from .mixins import IsAuthorMixin
from .models import Project


@login_required
def participate(request, pk):
    project = get_object_or_404(Project, id=pk)
    user = request.user
    if project.owner == user:
        return JsonResponse({'status': 'You are owner'})
    participating = project.participants.filter(id=user.id).exists()
    if participating:
        project.participants.remove(user)
    else:
        project.participants.add(user)
    return JsonResponse({"status": "ok", "participant": not participating})


@login_required
@require_http_methods(["POST"])
def project_complete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.status = STATUS_CLOSED
    project.save()
    return JsonResponse({"status": "ok"})


class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    queryset = Project.objects.prefetch_related(
        'participants'
    ).select_related('owner')
    paginate_by = PAGINATION
    ordering = ['-created_at']


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/create-project.html'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project-details.html'


class ProjectUpdateView(LoginRequiredMixin, IsAuthorMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/create-project.html'
