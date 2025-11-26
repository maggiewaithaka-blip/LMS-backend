from django.contrib import admin
from django.http import HttpResponse
import csv

## Removed GradeItem and Grade imports


## Removed GradeInline


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


## Removed GradeItemAdmin


## Removed GradeAdmin
    list_filter = ('item',)
    search_fields = ('user__username',)
    actions = [export_as_csv_action(fields=['id', 'item_id', 'user_id', 'value'])]
