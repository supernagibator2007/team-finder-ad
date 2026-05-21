from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, name, surname, password, **kwargs):
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, surname=surname, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, name, surname, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        return self.create_user(email, name, surname, password, **kwargs)
