from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import RegisterSerializer, UserSerializer, UserUpdateSerializer
from .permissions import IsAdmin


class RegisterView(generics.CreateAPIView):
    """Public registration — creates a Viewer by default."""
    queryset         = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class UserListView(generics.ListAPIView):
    """Admin only — list all users."""
    queryset           = User.objects.all().order_by('date_joined')
    serializer_class   = UserSerializer
    permission_classes = [IsAdmin]


class UserDetailView(generics.RetrieveUpdateAPIView):
    """
    GET  — any authenticated user can see their own profile.
    PATCH — admin can update any user's role/status.
    """
    queryset         = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return UserUpdateSerializer
        return UserSerializer

    def get_permissions(self):
        if self.request.method in ('PUT', 'PATCH'):
            return [IsAdmin()]
        return super().get_permissions()

    def get_object(self):
        pk = self.kwargs.get('pk')
        # Non-admins can only view themselves
        if self.request.user.role != 'admin':
            return self.request.user
        return super().get_object()