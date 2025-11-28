import nested_admin
from django.contrib import admin
from .models import CourseCategory, Course, CourseSection, Assignment, Quiz, Resource, Attachment

def export_as_csv_action(description="Export selected objects as CSV", fields=None):
    def export_as_csv(modeladmin, request, queryset):
        field_names = fields or [f.name for f in modeladmin.model._meta.fields]
        from django.http import HttpResponse
        import csv
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
    list_display = ('id', 'fullname', 'owner')
    search_fields = ('fullname', 'owner__username')


class AttachmentInline(nested_admin.NestedStackedInline):
    model = Attachment
    extra = 1
    fields = ('type', 'file', 'url', 'text')
    verbose_name = 'Attachment'
    verbose_name_plural = 'Attachments'

class ResourceInline(nested_admin.NestedStackedInline):
    model = Resource
    extra = 1
    inlines = [AttachmentInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'text'),
        }),
    )

class AssignmentInline(nested_admin.NestedStackedInline):
    model = Assignment
    extra = 1
    inlines = [AttachmentInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'text'),
        }),
    )

class QuizInline(nested_admin.NestedStackedInline):
    model = Quiz
    extra = 1
    inlines = [AttachmentInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'text'),
        }),
    )

@admin.register(CourseSection)
class CourseSectionAdmin(nested_admin.NestedModelAdmin):
    list_display = ('id', 'title', 'course', 'position')
    search_fields = ('title', 'course__fullname')
    inlines = [AssignmentInline, QuizInline, ResourceInline]

