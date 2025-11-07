from django.contrib import admin
from django.http import HttpResponse
import csv

from .models import Message, Notification


def export_as_csv_action(description="Export selected objects as CSV", fields=None):
    def export_as_csv(modeladmin, request, queryset):
        field_names = fields or [f.name for f in modeladmin.model._meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={modeladmin.model._meta.model_name}.csv'
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            row = [getattr(obj, f) for f in field_names]
            writer.writerow(row)
        return response

    export_as_csv.short_description = description
    return export_as_csv


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'recipient', 'subject', 'sent_at', 'read')
    list_filter = ('read',)
    search_fields = ('sender__username', 'recipient__username', 'subject')
    readonly_fields = ('sent_at',)
    actions = [export_as_csv_action(fields=['id', 'sender_id', 'recipient_id', 'subject', 'sent_at', 'read'])]


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'created_at', 'read')
    list_filter = ('read',)
    search_fields = ('user__username', 'title')
    readonly_fields = ('created_at',)
    actions = [export_as_csv_action(fields=['id', 'user_id', 'title', 'created_at', 'read'])]
