from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Message, Notification
from .serializers import MessageSerializer, NotificationSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('id')
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all().order_by('id')
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
