from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import TimeStampedModel


class User(TimeStampedModel, AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        PROVIDER = "PROVIDER", "Provider"
        CLIENT = "CLIENT", "Client"


    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.CLIENT,
    )

    @property
    def is_provider(self):
        return self.role == self.Roles.PROVIDER

    @property
    def is_admin(self):
        return self.role == self.Roles.ADMIN

    @property
    def is_client(self):
        return self.role == self.Roles.CLIENT

    def __str__(self):
        return f"{self.username} ({self.role})"