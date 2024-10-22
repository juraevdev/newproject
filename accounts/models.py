from django.db import models
from django.contrib.auth.models import AbstractUser
from accounts.managers import CustomUserManager

# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number',]

