from django.contrib import admin
from django.http import HttpResponse
import csv

from .models import CourseCategory, Course, CourseSection
from assignments.models import Attachment

class AssignmentAttachmentInline(admin.TabularInline):
    model = CourseSection.assignments.through
    extra = 1

class QuizAttachmentInline(admin.TabularInline):
    model = CourseSection.quizzes.through
    extra = 1

class ResourceAttachmentInline(admin.TabularInline):
    model = CourseSection.resources.through
    extra = 1


class CourseSectionInline(admin.TabularInline):
    model = CourseSection
    extra = 0
    fields = ('title', 'summary', 'position')
    readonly_fields = ()




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


@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent')
    search_fields = ('name',)
    actions = [export_as_csv_action(fields=['id', 'name', 'parent_id'])]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'shortname', 'fullname', 'visible', 'start_date', 'end_date')
    list_filter = ('visible', 'category')
    search_fields = ('shortname', 'fullname')
    inlines = [CourseSectionInline]
    actions = [export_as_csv_action(fields=['id', 'shortname', 'fullname', 'visible', 'start_date', 'end_date'])]


@admin.register(CourseSection)
class CourseSectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'title', 'position')
    list_filter = ('course',)
    inlines = [AssignmentAttachmentInline, QuizAttachmentInline, ResourceAttachmentInline]
    actions = [export_as_csv_action(fields=['id', 'course_id', 'title', 'position'])]






