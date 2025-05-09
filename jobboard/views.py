from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, status, serializers
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Job, Application, User
from .serializers import JobSerializer, ApplicationSerializer, UserSerializer

User = get_user_model()
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

# Retrieve, Update, Delete
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_object(self):
        obj = super().get_object()
        user = self.request.user

        # Employers can access all users
        if user.is_employer:
            return obj

        # Job seekers can only access their own data
        if obj != user:
            raise PermissionDenied("You are not allowed to access this user.")

        return obj

# Optional: To get a list of users (Read)
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.is_employer:
            raise PermissionDenied("Only employers can view the list of users.")
        return User.objects.all()

class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.is_employer:
            return Job.objects.filter(created_by=user)
        return Job.objects.all()  # Optional: show all jobs to public or seekers

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_employer:
            # Show only applications for jobs created by this employer
            return Application.objects.filter(job__created_by=user)
        else:
            # Show only applications made by this job seeker
            return Application.objects.filter(applicant=user)

    def perform_create(self, serializer):
        user = self.request.user
        job_id = self.request.data.get('job')

        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            raise serializers.ValidationError("Job not found.")

        # Check if the user has already applied for this job
        if Application.objects.filter(job=job, applicant=user).exists():
            raise serializers.ValidationError("You have already applied for this job.")

        serializer.save(applicant=user, job=job)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        application = self.get_object()
        if application.job.created_by != request.user:
            return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
        application.status = 'accepted'
        application.save()
        return Response({"status": "accepted"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        application = self.get_object()
        if application.job.created_by != request.user:
            return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
        application.status = 'rejected'
        application.save()
        return Response({"status": "rejected"}, status=status.HTTP_200_OK)




# Create your views here.
