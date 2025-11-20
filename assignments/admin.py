from django.contrib import admin
from django.http import HttpResponse
import csv

from .models import Assignment, Submission, AssignmentGrade


class SubmissionInline(admin.TabularInline):
    model = Submission
    extra = 0
    readonly_fields = ('submitted_at',)


class AssignmentGradeInline(admin.TabularInline):
    model = AssignmentGrade
    extra = 0


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


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'title', 'due_date')
    list_filter = ('course',)
    search_fields = ('title',)
    inlines = [SubmissionInline]
    actions = [export_as_csv_action(fields=['id', 'course_id', 'title', 'due_date'])]


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'assignment', 'user', 'submitted_at')
    list_filter = ('assignment', 'user')
    search_fields = ('assignment__title', 'user__username')
    readonly_fields = ('submitted_at',)
    inlines = [AssignmentGradeInline]
    actions = [export_as_csv_action(fields=['id', 'assignment_id', 'user_id', 'submitted_at'])]


@admin.register(AssignmentGrade)
class AssignmentGradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'submission', 'grader', 'score')
    search_fields = ('submission__assignment__title',)
    actions = [export_as_csv_action(fields=['id', 'submission_id', 'grader_id', 'score'])]
