from rest_framework import serializers
from .models import Enrollment, EnrollmentMethod


class EnrollmentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnrollmentMethod
        fields = ['id', 'name', 'config']


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['id', 'user', 'course', 'method', 'enrolled_at', 'role']
        read_only_fields = ['id', 'enrolled_at']
