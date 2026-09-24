from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        OWNER = 'OWNER', 'Property Owner'
        TENANT = 'TENANT', 'Tenant'
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.TENANT
    )
    phone = models.CharField(
        max_length=20,
        blank=True
    )

    profile_image = models.ImageField(
        upload_to='profile/',
        blank=True,
        null=True
    )

    address = models.CharField(
        max_length=255,
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    bio = models.TextField(
        blank=True
    )
    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"