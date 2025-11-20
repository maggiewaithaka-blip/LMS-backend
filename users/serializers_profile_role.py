from rest_framework import serializers
from .models import Profile, Role


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'id', 'user', 'passport_photo', 'national_id', 'passport', 'academic_certificate',
            'email', 'phone', 'qualification_level', 'field_of_study', 'nationality'
        ]
        read_only_fields = ['id', 'user']

    def validate(self, data):
        nationality = data.get('nationality', '').strip().lower()
        national_id = data.get('national_id')
        passport = data.get('passport')
        if nationality == 'kenyan':
            if not national_id:
                raise serializers.ValidationError({
                    'national_id': 'National ID is required for Kenyan applicants.'
                })
        else:
            if not passport:
                raise serializers.ValidationError({
                    'passport': 'Passport is required for non-Kenyan applicants.'
                })
        return data


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'shortname']
        read_only_fields = ['id']
