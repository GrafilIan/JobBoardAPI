from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, status
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
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically assign the user who is making the request to the applicant field
        user = self.request.user  # The user who is authenticated
        # Get the job ID from the serializer data and assign it to the application
        job_id = self.request.data.get('job')  # Retrieve the job ID from the request
        job = Job.objects.get(id=job_id)  # Fetch the job object

        serializer.save(applicant=user, job=job)  # Save the application with both applicant and job

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        application = self.get_object()
        application.status = 'accepted'
        application.save()
        return Response({"status": "accepted"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        application = self.get_object()
        application.status = 'rejected'
        application.save()
        return Response({"status": "rejected"}, status=status.HTTP_200_OK)


# Create your views here.
