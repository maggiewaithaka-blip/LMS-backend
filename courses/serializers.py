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
from .models_resource import Assignment, Quiz, Resource

from rest_framework import serializers

def get_attachment_serializer():
    from assignments.serializers import AttachmentSerializer
    return AttachmentSerializer

class AssignmentSerializer(serializers.ModelSerializer):
    attachments = serializers.SerializerMethodField()
    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'attachments']
    def get_attachments(self, obj):
        AttachmentSerializer = get_attachment_serializer()
        return AttachmentSerializer(obj.attachments.all(), many=True, read_only=True).data

class QuizSerializer(serializers.ModelSerializer):
    attachments = serializers.SerializerMethodField()
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'attachments']
    def get_attachments(self, obj):
        AttachmentSerializer = get_attachment_serializer()
        return AttachmentSerializer(obj.attachments.all(), many=True, read_only=True).data

class ResourceSerializer(serializers.ModelSerializer):
    attachments = serializers.SerializerMethodField()
    class Meta:
        model = Resource
        fields = ['id', 'title', 'description', 'attachments']
    def get_attachments(self, obj):
        AttachmentSerializer = get_attachment_serializer()
        return AttachmentSerializer(obj.attachments.all(), many=True, read_only=True).data

class CourseSectionSerializer(serializers.ModelSerializer):
    assignments = AssignmentSerializer(many=True, read_only=True)
    quizzes = QuizSerializer(many=True, read_only=True)
    resources = ResourceSerializer(many=True, read_only=True)
    class Meta:
        model = CourseSection
        fields = ['id', 'course', 'title', 'summary', 'position', 'assignments', 'quizzes', 'resources']



