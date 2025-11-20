from rest_framework import serializers
from .models_application import StudentApplication

class StudentApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentApplication
        fields = [
            'id', 'full_name', 'email', 'nationality', 'qualification', 'knqf_level',
            'academic_certificate', 'passport_photo', 'national_id', 'passport', 'submitted_at', 'status'
        ]
        read_only_fields = ['id', 'submitted_at', 'status']

    def validate(self, data):
        nationality = data.get('nationality', '').lower()
        if nationality == 'kenyan' and not data.get('national_id'):
            raise serializers.ValidationError({'national_id': 'National ID is required for Kenyan applicants.'})
        if nationality != 'kenyan' and not data.get('passport'):
            raise serializers.ValidationError({'passport': 'Passport is required for non-Kenyan applicants.'})
        return data
