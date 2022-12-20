from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractUser
from testapp.models import Course

class User(AbstractUser):
    CHOICES = [('S', 'Студент'), ('T', 'Викладач')]
    status = models.CharField(choices=CHOICES, max_length=1, default='S')
    pass