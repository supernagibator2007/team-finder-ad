from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'owner',
        'status',
        'created_at',
    )
    list_filter = ('created_at',)
    search_fields = ('name', 'owner__username')
    filter_horizontal = ('participants',)
    readonly_fields = ('created_at',)
