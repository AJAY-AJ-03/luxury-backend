from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models


class UserManager(BaseUserManager):
    """Custom manager for User model with email and phone support."""

    def create_user(self, username, email, phone_number, password=None, **extra_fields):
        if not username:
            raise ValueError('Username is required.')

        if not email:
            raise ValueError('Email is required.')

        if not phone_number:
            raise ValueError('Phone number is required.')

        email = self.normalize_email(email)

        user = self.model(
            username=username,
            email=email,
            phone_number=phone_number,
            **extra_fields,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(
            username=username,
            email=email,
            phone_number=phone_number,
            password=password,
            **extra_fields
        )


class User(AbstractUser):
    """
    Custom user model for ecommerce authentication.
    Supports login using email or phone number.
    """

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number']

    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message='Enter a valid phone number (9–15 digits, optional leading +).',
    )

    email = models.EmailField(
        unique=True,
    )

    phone_number = models.CharField(
        max_length=20,
        unique=True,
        validators=[phone_validator],
        help_text='Used for login alongside email.',
    )

    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.username