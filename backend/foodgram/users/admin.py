from django.contrib import admin
from users.models import User


class UserAdmin(admin.ModelAdmin):
    user_filter = ('email', 'username')


admin.site.register(User, UserAdmin)
