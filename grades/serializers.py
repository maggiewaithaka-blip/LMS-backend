from rest_framework import serializers
from .models import GradeItem, Grade


class GradeItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeItem
        fields = ['id', 'course', 'name', 'weight']


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['id', 'item', 'user', 'value', 'feedback']
