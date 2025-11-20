from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile

User = get_user_model()


# Serializer for nested Profile data within User
class ProfileSerializerForUser(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'gender', 'address', 'qualification_level', 'profile_picture']


# Registration serializer
class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField(required=False, allow_blank=True)
    timezone = serializers.CharField(required=False, allow_blank=True)
    institution = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'timezone', 'institution', 'phone']
        read_only_fields = ['id']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        # Ensure a profile is created for the new user
        Profile.objects.get_or_create(user=user)
        return user


# Login serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializerForUser()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'timezone', 'phone', 'institution', 'profile']
        read_only_fields = ['id', 'username']

    def update(self, instance, validated_data):
        # Handle nested profile data
        profile_data = validated_data.pop('profile', {})
        # Use get_or_create to robustly handle users that may not have a profile yet
        profile, created = Profile.objects.get_or_create(user=instance)

        # Update User fields
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.timezone = validated_data.get('timezone', instance.timezone)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.institution = validated_data.get('institution', instance.institution)
        instance.save()

        # Update Profile fields
        profile.date_of_birth = profile_data.get('date_of_birth', profile.date_of_birth)
        profile.gender = profile_data.get('gender', profile.gender)
        profile.address = profile_data.get('address', profile.address)
        profile.qualification_level = profile_data.get('qualification_level', profile.qualification_level)
        profile.profile_picture = profile_data.get('profile_picture', profile.profile_picture)
        profile.save()

        return instance
