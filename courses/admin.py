from django.contrib import admin
from django.http import HttpResponse
import csv

from .models import CourseCategory, Course, CourseSection, CourseModule, Lesson
from .models_resource import CourseResource


class CourseSectionInline(admin.TabularInline):
    model = CourseSection
    extra = 0
    fields = ('title', 'summary', 'position')
    readonly_fields = ()


class CourseModuleInline(admin.TabularInline):
    model = CourseModule
    extra = 0
    fields = ('name', 'module_type', 'visible')


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
    inlines = [CourseModuleInline]
    actions = [export_as_csv_action(fields=['id', 'course_id', 'title', 'position'])]


@admin.register(CourseModule)
class CourseModuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'section', 'name', 'module_type', 'visible')
    list_filter = ('module_type', 'visible')
    actions = [export_as_csv_action(fields=['id', 'section_id', 'name', 'module_type', 'visible'])]


@admin.register(CourseResource)
class CourseResourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'title', 'resource_type', 'file', 'url', 'created_at')
    list_filter = ('resource_type', 'course')
    search_fields = ('title', 'course__shortname')
    actions = [export_as_csv_action(fields=['id', 'course_id', 'title', 'resource_type', 'file_id', 'url', 'created_at'])]
