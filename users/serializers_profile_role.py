from rest_framework import serializers
from .models import Profile, Role


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'extra_data']
        read_only_fields = ['id', 'user']


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'shortname']
        read_only_fields = ['id']
