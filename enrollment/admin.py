from django.contrib import admin
from django.http import HttpResponse
import csv

from .models import EnrollmentMethod, Enrollment


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


@admin.register(EnrollmentMethod)
class EnrollmentMethodAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    actions = [export_as_csv_action(fields=['id', 'name'])]


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course', 'method', 'enrolled_at', 'role')
    list_filter = ('course', 'role')
    search_fields = ('user__username', 'course__shortname')
    readonly_fields = ('enrolled_at',)
    actions = [export_as_csv_action(fields=['id', 'user_id', 'course_id', 'method_id', 'enrolled_at', 'role'])]
