from django.contrib import admin
from django.http import HttpResponse
import csv

from .models import Quiz, Question, QuizAttempt, QuestionResponse


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 0
    fields = ('question_type', 'text', 'data')


class QuestionResponseInline(admin.TabularInline):
    model = QuestionResponse
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


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('id', 'course', 'title', 'time_limit', 'attempts_allowed')
    list_filter = ('course',)
    search_fields = ('title',)
    inlines = [QuestionInline]
    actions = [export_as_csv_action(fields=['id', 'course_id', 'title'])]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'quiz', 'question_type')
    search_fields = ('quiz__title', 'text')


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ('id', 'quiz', 'user', 'started_at', 'completed_at', 'score')
    list_filter = ('quiz', 'user')
    inlines = [QuestionResponseInline]
    readonly_fields = ('started_at', 'completed_at')
    actions = [export_as_csv_action(fields=['id', 'quiz_id', 'user_id', 'score'])]


@admin.register(QuestionResponse)
class QuestionResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'attempt', 'question', 'correct')
    actions = [export_as_csv_action(fields=['id', 'attempt_id', 'question_id', 'correct'])]
