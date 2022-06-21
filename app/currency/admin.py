from currency.models import ContactUs, Source

from django.contrib import admin


class SourceAdmin(admin.ModelAdmin):
    # отображение колонок
    list_display = (
        'name',
        'code_name',
        'source_url',
        'logotype',
    )
    # только для чтения
    readonly_fields = (
        'name',
        'code_name',
    )


class ContactUsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email_from',
        'subject',
        'message',
    )

    readonly_fields = (
        'email_from',
        'subject',
        'message',
    )

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(Source, SourceAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
