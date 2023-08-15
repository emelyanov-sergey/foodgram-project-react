from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin

from users.models import MyUser


@register(MyUser)
class MyUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('email', 'username')
    search_fields = ('email', 'username')
