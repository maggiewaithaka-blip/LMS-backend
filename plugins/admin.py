from django.contrib import admin
from django.http import HttpResponse
import csv

from .models import Plugin, SystemConfig


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


@admin.register(Plugin)
class PluginAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'enabled', 'installed_at')
    list_filter = ('enabled',)
    search_fields = ('name',)
    actions = [export_as_csv_action(fields=['id', 'name', 'enabled', 'installed_at'])]


@admin.register(SystemConfig)
class SystemConfigAdmin(admin.ModelAdmin):
    list_display = ('id', 'key', 'updated_at')
    search_fields = ('key',)
    readonly_fields = ('updated_at',)
    actions = [export_as_csv_action(fields=['id', 'key', 'updated_at'])]
