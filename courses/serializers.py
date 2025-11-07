from rest_framework import serializers
from .models import Course, CourseCategory, CourseSection, CourseModule


class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCategory
        fields = ['id', 'name', 'parent']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'shortname', 'fullname', 'summary', 'visible', 'start_date', 'end_date', 'category']


class CourseSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSection
        fields = ['id', 'course', 'title', 'summary', 'position']


class CourseModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseModule
        fields = ['id', 'section', 'name', 'module_type', 'visible']
