from rest_framework import serializers
from .models import Course, CourseCategory, CourseSection
from .models import Assignment, Quiz, Resource # Assuming Assignment, Quiz, Resource are in .models now

# REMOVED: from assignments.serializers import AttachmentSerializer

# --- Core Serializers ---

class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['id', 'name', 'parent']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'shortname', 'fullname', 'summary', 'visible', 'start_date', 'end_date', 'category']


# --- Helper Functions for Deferral ---

# Define the deferred serialization logic once to keep the code clean.
# This avoids repeating the get_attachments method in all three serializers.
def get_deferred_attachments(serializer_instance, obj):
    """Handles the deferred import and serialization of attachments."""
    # Local, deferred import to run at runtime, not startup
    from assignments.serializers import AttachmentSerializer
    attachments_qs = obj.attachments.all()
    # Pass the context from the outer serializer instance
    return AttachmentSerializer(attachments_qs, many=True, context=serializer_instance.context).data


# --- Nested Serializers with Circular Dependency Fix ---

class AssignmentSerializer(serializers.ModelSerializer):
    # FIX: Define SerializerMethodField directly on the class.
    attachments = serializers.SerializerMethodField()

    def get_attachments(self, obj):
        # Delegate to the helper function which handles the deferred import
        return get_deferred_attachments(self, obj)

    class Meta:
        model = Assignment
        fields = ['id', 'title', 'description', 'attachments']


class QuizSerializer(serializers.ModelSerializer):
    # FIX: Define SerializerMethodField directly on the class.
    attachments = serializers.SerializerMethodField()

    def get_attachments(self, obj):
        return get_deferred_attachments(self, obj)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'attachments']


class ResourceSerializer(serializers.ModelSerializer):
    # FIX: Define SerializerMethodField directly on the class.
    attachments = serializers.SerializerMethodField()

    def get_attachments(self, obj):
        return get_deferred_attachments(self, obj)

    class Meta:
        model = Resource
        fields = ['id', 'title', 'description', 'attachments']

# --- Course Section Serializer ---

class CourseSectionSerializer(serializers.ModelSerializer):
    assignments = AssignmentSerializer(many=True, read_only=True)
    quizzes = QuizSerializer(many=True, read_only=True)
    resources = ResourceSerializer(many=True, read_only=True)

    class Meta:
        model = CourseSection
        fields = ['id', 'course', 'title', 'summary', 'position', 'assignments', 'quizzes', 'resources']