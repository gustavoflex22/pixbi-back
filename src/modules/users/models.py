from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    forgot_password_uuid = models.UUIDField(null=True)
    accepted_terms = models.BooleanField(default=False)