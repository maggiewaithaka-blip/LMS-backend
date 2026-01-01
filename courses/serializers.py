from rest_framework import serializers
from .models import Course, CourseCategory, CourseSection, Assignment, Quiz, Resource, Attachment

class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['id', 'name', 'parent']

class CourseSerializer(serializers.ModelSerializer):
    thumbnail = serializers.ImageField(read_only=True)
    class Meta:
        model = Course
        fields = ['id', 'shortname', 'fullname', 'summary', 'visible', 'start_date', 'end_date', 'category', 'thumbnail']


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['id', 'type', 'file', 'url', 'text']

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
    resources = ResourceSerializer(many=True, read_only=True)
    assignments = AssignmentSerializer(many=True, read_only=True)
    quizzes = QuizSerializer(many=True, read_only=True)
    class Meta:
        model = CourseSection
        fields = ['id', 'title', 'summary', 'course', 'position', 'notifications', 'storage', 'resources', 'assignments', 'quizzes']