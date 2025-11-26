import nested_admin

from .models import CourseCategory, Course, CourseSection
from assignments.models import Attachment
from .models_resource import Assignment, Quiz, Resource



# Nested inline for Assignment attachments (FK-based)
class AssignmentAttachmentInline(nested_admin.NestedTabularInline):
    model = Attachment
    extra = 1
    verbose_name = "Assignment Attachment"
    fk_name = 'assignment'
    # fields removed, only fieldsets used
    fieldsets = (
        (None, {
            'fields': ('type', 'file', 'url', 'text'),
        }),
    )



# Nested inline for Quiz attachments (FK-based)
class QuizAttachmentInline(nested_admin.NestedTabularInline):
    model = Attachment
    extra = 1
    verbose_name = "Quiz Attachment"
    fk_name = 'quiz'
    # fields removed, only fieldsets used
    fieldsets = (
        (None, {
            'fields': ('type', 'file', 'url', 'text'),
        }),
    )



# Nested inline for Resource attachments (FK-based)
class ResourceAttachmentInline(nested_admin.NestedTabularInline):
    model = Attachment
    extra = 1
    verbose_name = "Resource Attachment"
    fk_name = 'resource'
    # fields removed, only fieldsets used
    fieldsets = (
        (None, {
            'fields': ('type', 'file', 'url', 'text'),
        }),
    )
from django.contrib import admin
from django.http import HttpResponse
import csv

from .models import CourseCategory, Course, CourseSection
from assignments.models import Attachment




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





# Nested inline for Assignments in CourseSection (FK-based)
class AssignmentInline(nested_admin.NestedTabularInline):
    model = Assignment
    extra = 1
    verbose_name = "Assignment"
    inlines = [AssignmentAttachmentInline]



# Nested inline for Quizzes in CourseSection (FK-based)
class QuizInline(nested_admin.NestedTabularInline):
    model = Quiz
    extra = 1
    verbose_name = "Quiz"
    inlines = [QuizAttachmentInline]



# Nested inline for Resources in CourseSection (FK-based)
class ResourceInline(nested_admin.NestedTabularInline):
    model = Resource
    extra = 1
    verbose_name = "Resource"
    inlines = [ResourceAttachmentInline]


@admin.register(CourseSection)
class CourseSectionAdmin(nested_admin.NestedModelAdmin):
    list_display = ('id', 'course', 'title', 'position')
    list_filter = ('course',)
    inlines = [AssignmentInline, QuizInline, ResourceInline]
    actions = [export_as_csv_action(fields=['id', 'course_id', 'title', 'position'])]

# Register Assignment, Quiz, Resource with their attachment inlines
@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    inlines = [AssignmentAttachmentInline]

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    inlines = [QuizAttachmentInline]

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    inlines = [ResourceAttachmentInline]






