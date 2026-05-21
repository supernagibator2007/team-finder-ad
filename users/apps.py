from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = 'Эксплуатант'
    verbose_name_plural = 'Эксплуатанты'
