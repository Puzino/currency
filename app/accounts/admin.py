from accounts.models import User

from django.contrib import admin


class UserAdmin(admin.ModelAdmin):
    search_fields = ['email']
    # отображение колонок
    list_display = (
        'email',
        'phone',
        'username',
        'is_superuser',
        'is_active',
    )


admin.site.register(User, UserAdmin)
