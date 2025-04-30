from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, JobViewSet, ApplicationViewSet, UserListView, UserDetailView

router = DefaultRouter()
router.register(r'jobs', JobViewSet, basename='job')
router.register(r'applications', ApplicationViewSet, basename='application')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', UserListView.as_view(), name='user_list'),      # Get list of users
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),  # Retrieve, Update, Delete a user
    path('', include(router.urls)),
]
