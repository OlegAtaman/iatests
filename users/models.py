from django.contrib.auth.models import AbstractUser
from django.db import models

from testapp.models import Course


class User(AbstractUser):
    full_name = models.CharField(max_length=50, null=True)
    CHOICES = [("S", "Студент"), ("T", "Викладач")]
    status = models.CharField(choices=CHOICES, max_length=1, default="S")
