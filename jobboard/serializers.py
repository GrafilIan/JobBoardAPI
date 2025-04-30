from rest_framework import serializers
from .models import User, Job, Application

# Serializer for the User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_employer']
        extra_kwargs = {'is_active': {'default': True}}

# Serializer for the Job model
class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'location', 'salary']

# Serializer for the Application model
class ApplicationSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)  # Embed Job details in the Application serializer
    applicant = UserSerializer(read_only=True)  # Embed User details in the Application serializer

    class Meta:
        model = Application
        fields = ['id', 'job', 'applicant', 'cover_letter', 'status', 'applied_at']
