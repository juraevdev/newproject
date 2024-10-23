from django.contrib.auth.models import UserManager
from django.contrib.auth.hashers import make_password

class CustomUserManager(UserManager):
    def _create_user(self, username, phone_number, password, **extra_fields):
        if not username:
            raise ValueError("The username must be set")
        if not phone_number:
            raise ValueError("The phone number must be set")
        user = self.model(username=username, phone_number=phone_number, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, phone_number, password, **extra_fields)

    def create_superuser(self, username, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, phone_number, password, **extra_fields)