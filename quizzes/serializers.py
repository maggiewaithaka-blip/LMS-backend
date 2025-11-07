from rest_framework import serializers
from .models import Quiz, Question, QuizAttempt, QuestionResponse


class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'course', 'title', 'description', 'time_limit', 'attempts_allowed']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'quiz', 'question_type', 'text', 'data']


class QuizAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAttempt
        fields = ['id', 'quiz', 'user', 'started_at', 'completed_at', 'score', 'data']
        read_only_fields = ['started_at']


class QuestionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionResponse
        fields = ['id', 'attempt', 'question', 'answer', 'correct']
