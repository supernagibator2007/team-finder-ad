from django.contrib.auth import get_user_model
from django.urls import reverse
from django.db import models

User = get_user_model()

class Project(models.Model):
    STATUS = [("open", "Open"), ("closed", "Closed")]
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_projects'
    )
    created_at = models.DateField(auto_now_add=True)
    github_url = models.URLField(
        blank=True,
        null=True,
        verbose_name='Ссылка на GitHub'
    )
    status = models.CharField(
        max_length=6,
        choices=STATUS,
        verbose_name='Статус'
    )
    participants = models.ManyToManyField(
        User,
        blank=True,
        related_name='participated_projects'
    )

    def get_absolute_url(self):
        return reverse("projects:detail", kwargs={"pk": self.pk})
