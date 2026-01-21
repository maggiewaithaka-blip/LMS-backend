import nested_admin
from django.contrib import admin
from .models import CourseCategory, Course, CourseSection, Assignment, Quiz, Resource, Attachment
from .models_scorm import ScormPackage
import zipfile
from django.conf import settings
import os
from django.http import HttpResponse
import csv


class ScormPackageInline(nested_admin.NestedStackedInline):
    model = ScormPackage
    extra = 1
    fieldsets = (
        (None, {
            'fields': ('name', 'zip_file'),
        }),
    )


# --- CSV export action ---
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

# --- CourseCategory Admin ---
@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent')
    list_display_links = ('name',)  # Make name clickable for edit
    search_fields = ('name',)
    actions = [export_as_csv_action(fields=['id', 'name', 'parent_id'])]

# --- Course Admin ---
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'owner')
    list_display_links = ('fullname',)  # Make fullname clickable for edit
    search_fields = ('fullname', 'owner__username')
    fields = ('shortname', 'fullname', 'summary', 'visible', 'start_date', 'end_date', 'category', 'owner', 'thumbnail')

# --- Nested Admin Inlines ---
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

# --- CourseSection Admin ---
@admin.register(CourseSection)
class CourseSectionAdmin(nested_admin.NestedModelAdmin):
    list_display = ('id', 'title', 'course', 'position')
    list_display_links = ('title',)  # Make title clickable for edit
    search_fields = ('title', 'course__fullname')
    list_filter = ('course',)
    inlines = [ResourceInline, AssignmentInline, QuizInline, ScormPackageInline]



@admin.register(ScormPackage)
class ScormPackageAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "section", "uploaded_at")
    search_fields = ("name",)
    fields = ("section", "name", "zip_file", "uploaded_at")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Only extract if zip_file is present and extraction dir does not exist
        extract_dir = os.path.join(settings.MEDIA_ROOT, 'scorm', f'scorm_{obj.pk}')
        if obj.zip_file and not os.path.exists(extract_dir):
            os.makedirs(extract_dir, exist_ok=True)
            with zipfile.ZipFile(obj.zip_file.path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)