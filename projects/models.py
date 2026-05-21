from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from utils.const import (MAX_LENGTH_PROJECT, MAX_LENGTH_STATUS, STATUS_CLOSED,
                         STATUS_OPENED)

User = get_user_model()


class Project(models.Model):
    STATUS = [(STATUS_OPENED, "Открыт"), (STATUS_CLOSED, "Закрыт")]
    name = models.CharField(
        max_length=MAX_LENGTH_PROJECT,
        verbose_name='Название'
    )
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
        max_length=MAX_LENGTH_STATUS,
        choices=STATUS,
        verbose_name='Статус',
        default=STATUS_CLOSED
    )
    participants = models.ManyToManyField(
        User,
        blank=True,
        related_name='participated_projects',
        verbose_name='Участники'
    )

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def get_absolute_url(self):
        return reverse("projects:detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f'{self.name}, автор - {self.owner}'
