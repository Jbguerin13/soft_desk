from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom user model with additional fields.
    """
    age = models.PositiveIntegerField(null=True, blank=True)
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.age and self.age < 15:
            raise ValueError("Users less than 15 years old can't subscribe.")
        super().save(*args, **kwargs)
