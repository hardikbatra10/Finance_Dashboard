from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        VIEWER   = 'viewer',  'Viewer'
        ANALYST  = 'analyst', 'Analyst'
        ADMIN    = 'admin',   'Admin'

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.VIEWER)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.username} ({self.role})'