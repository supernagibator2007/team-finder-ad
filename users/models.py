import io
import os
import random

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image, ImageDraw, ImageFont
from utils.const import (MAX_LENGTH_ABOUT, MAX_LENGTH_NAME, MAX_LENGTH_PHONE,
                         MAX_LENGTH_SKILL)

from .managers import UserManager


font_path = os.path.join(settings.BASE_DIR, 'static',
                         'fonts', 'Neue_Haas_Grotesk_Display_Pro_75_Bold.otf')


class Skill(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_SKILL, verbose_name='Навык')

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=MAX_LENGTH_NAME, verbose_name='Имя')
    surname = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name='Фамилия'
    )
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone = models.CharField(
        max_length=MAX_LENGTH_PHONE,
        blank=True,
        null=True,
        verbose_name='Номер телефона'
    )
    github_url = models.URLField(
        blank=True, null=True, verbose_name='Ссылка на профиль GitHub:'
    )
    about = models.TextField(
        max_length=MAX_LENGTH_ABOUT,
        blank=True,
        null=True,
        verbose_name='Обо мне'
    )
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

    class Meta:
        verbose_name = 'Эксплуатант'
        verbose_name_plural = 'Эксплуатанты'

    def save(self, *args, **kwargs):
        if self.avatar:
            return super().save(*args, **kwargs)
        first_letter = self.name[0].upper()
        bg_color = random.choice([
            (74, 144, 226),
            (46, 204, 113),
            (231, 76, 60),
            (155, 89, 182),
            (241, 196, 15),
            (52, 73, 94)
        ])
        img_size = 200
        image = Image.new('RGB', (img_size, img_size), color=bg_color)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(font_path, 110)
        left, top, right, bottom = draw.textbbox(
            (0, 0), first_letter, font=font)
        text_width = right - left
        text_height = bottom - top
        x = (img_size - text_width) / 2
        y = (img_size - text_height) / 2 - top
        draw.text((x, y), first_letter, fill=(255, 255, 255), font=font)
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        filename = f"avatar_{self.email}.png"
        self.avatar.save(filename, ContentFile(buffer.getvalue()), save=False)
        super().save(*args, **kwargs)
