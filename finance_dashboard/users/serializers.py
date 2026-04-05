from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model  = User
        fields = ('id', 'username', 'email', 'password', 'role')
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ('id', 'username', 'email', 'role', 'is_active', 'date_joined')
        read_only_fields = ('id', 'date_joined')


class UserUpdateSerializer(serializers.ModelSerializer):
    """Admin can update role and status."""
    class Meta:
        model  = User
        fields = ('role', 'is_active')