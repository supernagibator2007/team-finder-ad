from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, CreateView, DetailView, UpdateView
)

from .models import Project
from .forms import ProjectForm



def project_complete(request, pk):
    if request.method == 'POST':
        project = get_object_or_404(Project, pk=pk)
        project.status = 'closed'
        project.save()
        return JsonResponse({"status": "ok", "project_status": "closed"})


class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
    paginate_by = 12
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


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/create-project.html'

    def test_func(self):
        project = self.get_object()
        return self.request.user == project.owner


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/create-project.html'

    def test_func(self):
        project = self.get_object()
        return self.request.user == project.owner