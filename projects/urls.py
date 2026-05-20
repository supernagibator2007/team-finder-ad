from django.urls import path

from . import views

app_name = 'projects'

urlpatterns = [
    path('<int:pk>/', views.ProjectDetailView.as_view(), name='detail'),
    path('<int:pk>/edit', views.ProjectUpdateView.as_view(), name='update'),
    path('<int:pk>/complete/', views.project_complete, name='complete'),
    path('<int:pk>/toggle-participate/', views.participate, name='participate'),
    path('create-project/', views.ProjectCreateView.as_view(), name='create'),
    path('list/', views.ProjectListView.as_view(), name='index'),
]
