from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'role',
        'bio',
        'first_name',
        'last_name'
    )
    list_display_links = (
        'username',
    )
    list_editable = (
        'role',
    )
    search_fields = ('username',)
    list_filter = ('role',)
    empty_value_display = 'Не задано'


admin.site.unregister(Group)
admin.site.empty_value_display = 'Не задано'
