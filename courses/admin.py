from django.contrib import admin
from .models_resource import Assignment, Quiz, Resource
from assignments.models import Attachment

class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 1

class AssignmentAdmin(admin.ModelAdmin):
    inlines = [AttachmentInline]

class QuizAdmin(admin.ModelAdmin):
    inlines = [AttachmentInline]

class ResourceAdmin(admin.ModelAdmin):
    inlines = [AttachmentInline]


import nested_admin
from django.contrib import admin
from django.http import HttpResponse
import csv

from .models import CourseCategory, Course, CourseSection
from assignments.models import Attachment
from .models_resource import Assignment, Quiz, Resource


import nested_admin
from django.contrib import admin
from .models import CourseCategory, Course, CourseSection
from .models_resource import Assignment, Quiz, Resource
from assignments.models import Attachment

# Nested inlines for attachments
class AssignmentAttachmentInline(nested_admin.NestedTabularInline):
    model = Attachment
    extra = 1
    fk_name = 'assignment'

class QuizAttachmentInline(nested_admin.NestedTabularInline):
    model = Attachment
    extra = 1
    fk_name = 'quiz'

class ResourceAttachmentInline(nested_admin.NestedTabularInline):
    model = Attachment
    extra = 1
    fk_name = 'resource'

# Nested inlines for assignments, quizzes, resources

class AssignmentInline(nested_admin.NestedTabularInline):
    model = Assignment
    extra = 1
    inlines = [AssignmentAttachmentInline]

class QuizInline(nested_admin.NestedTabularInline):
    model = Quiz
    extra = 1
    inlines = [QuizAttachmentInline]

class ResourceInline(nested_admin.NestedTabularInline):
    model = Resource
    extra = 1
    inlines = [ResourceAttachmentInline]

class CourseSectionAdmin(nested_admin.NestedModelAdmin):
    inlines = [AssignmentInline, QuizInline, ResourceInline]
    list_display = ('id', 'title', 'course', 'position')
    search_fields = ('title', 'course__fullname')

admin.site.register(CourseSection, CourseSectionAdmin)

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



# --- 4. Standalone Admin Registration (Using fixed Inlines) ---

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