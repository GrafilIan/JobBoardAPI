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
    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'location', 'salary']

class ApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_employer']  # Only necessary fields

# Serializer for the Application model
class ApplicationSerializer(serializers.ModelSerializer):
    job = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all())  # Use PrimaryKeyRelatedField
    applicant = UserSerializer(read_only=True)

    class Meta:
        model = Application
        fields = ['id', 'job', 'applicant', 'cover_letter', 'status', 'applied_at']
