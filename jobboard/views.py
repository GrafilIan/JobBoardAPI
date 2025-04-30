from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, status, serializers
from rest_framework.decorators import action
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
    lookup_field = 'pk'  # To use user ID for lookup

# Optional: To get a list of users (Read)
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return [permissions.AllowAny()]

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
