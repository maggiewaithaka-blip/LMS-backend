from rest_framework import serializers
from .models import Message, Notification


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'subject', 'body', 'sent_at', 'read']
        read_only_fields = ['id', 'sent_at']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'title', 'message', 'created_at', 'read']
        read_only_fields = ['id', 'created_at']
