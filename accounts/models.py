import random
import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from accounts.managers import CustomUserManager

# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number',]

    def __str__(self):
        return self.username
    
    def generate_verify_code(self):
        code = ''.join([str(random.randint(0, 100)%10) for _ in range(5)])
        UserConfirmation.objects.create(
            code = code,
            user = self,
            expires = timezone.now() + datetime.timedelta(minutes=2)
        )
        return code

class UserConfirmation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='codes')
    code = models.CharField(max_length=5)
    expires = models.DateTimeField(null=True, blank=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.code}"

class Intro(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title
