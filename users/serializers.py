from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile

User = get_user_model()


# Serializer for nested Profile data within User
# Profile serialization is disabled — profile management is handled outside the public API.
#class ProfileSerializerForUser(serializers.ModelSerializer):
#    profile_picture = serializers.SerializerMethodField()
#    passport_photo = serializers.SerializerMethodField()
#    national_id = serializers.SerializerMethodField()
#    passport = serializers.SerializerMethodField()
#    academic_certificate = serializers.SerializerMethodField()
#    field_of_study = serializers.CharField(required=False, allow_blank=True)
#    nationality = serializers.CharField(required=False, allow_blank=True)
#
#    class Meta:
#        model = Profile
#        fields = ['date_of_birth', 'gender', 'address', 'qualification_level', 'profile_picture', 'passport_photo', 'national_id', 'passport', 'academic_certificate', 'field_of_study', 'nationality']
#
#    def get_profile_picture(self, obj):
#        request = self.context.get('request')
#        if obj.profile_picture and hasattr(obj.profile_picture, 'url'):
#            return request.build_absolute_uri(obj.profile_picture.url)
#        return None
#
#    def get_passport_photo(self, obj):
#        request = self.context.get('request')
#        if obj.passport_photo and hasattr(obj.passport_photo, 'url'):
#            return request.build_absolute_uri(obj.passport_photo.url)
#        return None
#
#    def get_national_id(self, obj):
#        request = self.context.get('request')
#        if obj.national_id and hasattr(obj.national_id, 'url'):
#            return request.build_absolute_uri(obj.national_id.url)
#        return None
#
#    def get_passport(self, obj):
#        request = self.context.get('request')
#        if obj.passport and hasattr(obj.passport, 'url'):
#            return request.build_absolute_uri(obj.passport.url)
#        return None
#
#    def get_academic_certificate(self, obj):
#        request = self.context.get('request')
#        if obj.academic_certificate and hasattr(obj.academic_certificate, 'url'):
#            return request.build_absolute_uri(obj.academic_certificate.url)
#        return None


# Registration serializer
# Registration is disabled. New users are created by administrators/back-end only.
#class RegistrationSerializer(serializers.ModelSerializer):
#    password = serializers.CharField(write_only=True, min_length=8)
#    email = serializers.EmailField(required=False, allow_blank=True)
#    timezone = serializers.CharField(required=False, allow_blank=True)
#    institution = serializers.CharField(required=False, allow_blank=True)
#    phone = serializers.CharField(required=False, allow_blank=True)
#    class Meta:
#        model = User
#        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email', 'timezone', 'institution', 'phone']
#        read_only_fields = ['id']
#
#    def create(self, validated_data):
#        password = validated_data.pop('password')
#        user = User(**validated_data)
#        user.set_password(password)
#        user.save()
#        # Ensure a profile is created for the new user
#        Profile.objects.get_or_create(user=user)
#        return user


# Login serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):
    # Profile data removed from public API per client request.

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'timezone', 'phone', 'institution']
        read_only_fields = ['id', 'username']

    def update(self, instance, validated_data):
        # Update User fields only (no profile updates via API)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.timezone = validated_data.get('timezone', instance.timezone)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.institution = validated_data.get('institution', instance.institution)
        instance.save()
        return instance
