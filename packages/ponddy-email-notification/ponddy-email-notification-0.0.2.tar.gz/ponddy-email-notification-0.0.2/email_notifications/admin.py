from django.contrib import admin

from . import services
from .models import Status, Notification


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'uuid')
    list_filter = ('status',)
    readonly_fields = ('uuid',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('subject', 'status', 'create_at', 'finish_at')
    list_filter = ('status',)
    filter_horizontal = ('users',)
    add_fieldsets = (
        (None, {
            'fields': ('subject', 'message', 'html_message', 'users'),
        }),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets

        return super().get_fieldsets(request, obj)

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return (
                'finish_at', 'subject', 'message',
                'html_message', 'users', 'status', 'create_at',
            )

        return super().get_readonly_fields(request, obj)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        if form.instance.status == Notification.UNDONE:
            services.send_notification(request, form.instance)
