from rest_framework import serializers
from .models import Course, CourseCategory, CourseSection


class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['id', 'name', 'parent']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'shortname', 'fullname', 'summary', 'visible', 'start_date', 'end_date', 'category']



# --- Nested Serializers ---

from assignments.serializers import AttachmentSerializer
from .models_resource import Assignment, Quiz, Resource

class AssignmentSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True, read_only=True)
    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'attachments']

class QuizSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True, read_only=True)
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'attachments']

class ResourceSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True, read_only=True)
    class Meta:
        model = Resource
        fields = ['id', 'title', 'description', 'attachments']

class CourseSectionSerializer(serializers.ModelSerializer):
    assignments = AssignmentSerializer(many=True, read_only=True)
    quizzes = QuizSerializer(many=True, read_only=True)
    resources = ResourceSerializer(many=True, read_only=True)
    class Meta:
        model = CourseSection
        fields = ['id', 'course', 'title', 'summary', 'position', 'assignments', 'quizzes', 'resources']



