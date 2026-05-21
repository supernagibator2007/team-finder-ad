from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Skill, User


ADDITIONAL_USER_FIELDS = (
    ('Информация', {'fields': (
        'name', 'surname', 'avatar', 'phone', 'about', 'github_url',
        'skills', 'is_active', 'is_staff', 'is_superuser'
    )}),
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'name', 'surname',
                    'phone', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'skills')
    search_fields = ('email', 'name', 'surname', 'phone', 'github_url')
    ordering = ('id',)
    fieldsets = (
        ('Данные для входа', {'fields': ('email', 'password')}),
    ) + ADDITIONAL_USER_FIELDS
    add_fieldsets = (
        (None, {
            'fields': (
                'email', 'name', 'surname', 'password', 'is_staff', 'is_active'
            ),
        }),
    )
    # из-за того, что в fieldsets и add_fieldsets класса BaseUserAdmin
    # есть поля username и т.д., которых нет в моем, пришлось переопределить
    filter_horizontal = ('skills', 'user_permissions')


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)
