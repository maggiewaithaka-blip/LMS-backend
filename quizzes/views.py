from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Quiz, Question, QuizAttempt, QuestionResponse
from .serializers import QuizSerializer, QuestionSerializer, QuizAttemptSerializer, QuestionResponseSerializer


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all().order_by('id')
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by('id')
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class QuizAttemptViewSet(viewsets.ModelViewSet):
    queryset = QuizAttempt.objects.all().order_by('id')
    serializer_class = QuizAttemptSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class QuestionResponseViewSet(viewsets.ModelViewSet):
    queryset = QuestionResponse.objects.all().order_by('id')
    serializer_class = QuestionResponseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
