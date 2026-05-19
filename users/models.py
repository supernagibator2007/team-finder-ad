from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


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


class Skill(models.Model):
    name = models.CharField(max_length=124)

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=124)
    surname = models.CharField(max_length=124)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    about = models.TextField(max_length=256, blank=True, null=True)
    skills = models.ManyToManyField(
        Skill,
        blank=True,
        related_name='skills'
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']
