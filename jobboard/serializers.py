from rest_framework import serializers
from .models import User, Job, Application

# Serializer for the User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_employer']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # This properly hashes the password
        user.is_active = True  # Ensure the user is active by default
        user.save()
        return user

# Serializer for the Job model
class JobSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.username', read_only=True)
    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'location', 'salary', 'created_by']

class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # Only necessary fields

# Serializer for the Application model
class ApplicationSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)  # Use JobSerializer to show full job details
    applicant = ApplicantSerializer(read_only=True)  # Use ApplicantSerializer to show the reduced applicant fields

    class Meta:
        model = Application
        fields = ['id', 'job', 'applicant', 'cover_letter', 'file_upload', 'status', 'applied_at']

    def get_applicant(self, obj):
        # Only return selected applicant fields
        return {
            "username": obj.applicant.username,
            "email": obj.applicant.email
        }
