from django.urls import path, include, reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView

from . import views, forms

app_name = 'users'

urlpatterns = [
    path('<int:pk>/', views.UserDetailView.as_view(), name='detail'),
    path('<int:pk>/skills/<int:skill_pk>/remove/', views.remove_skill, name='remove-skill'),
    path('<int:pk>/skills/add/', views.add_skill, name='add-skill'),
    path('edit-profile/', views.UserUpdateView.as_view(), name='update'),
    path('list/', views.UserListView.as_view(), name='list'),
    path('login/', LoginView.as_view(
        template_name='users/login.html',
        form_class=forms.LoginForm,
        success_url=reverse_lazy('projects:index')
        ),
        name='login'),
    path('register/',
        CreateView.as_view(
            template_name='users/register.html',
            form_class=forms.CustomUserCreateForm,
            success_url=reverse_lazy('projects:index'),
        ),
        name='register'
    ),
    path('change-password/', views.UserPasswordChangeView.as_view(), name='change-password'),
    path('logout/', views.logout_view, name='logout'),
    path('skills/', views.skills_search, name='skills-search'),
]
