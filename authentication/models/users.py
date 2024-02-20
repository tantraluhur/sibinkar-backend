from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, password, phone_number, **kwargs):
        return self.create(phone_number=phone_number,
                           password=make_password(password),
                           **kwargs)

    def create_superuser(self, phone_number, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(phone_number=phone_number, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

    def get_user_by_phone(self, phone_number):
        return self.filter(phone_number=phone_number, is_active=True).last()

    def reset_password(self, phone_number, password):
        user = self.get_user_by_phone(phone_number)
        user.password = make_password(password)
        user.save()


class AuthUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=50, null=True)
    email = models.EmailField(_('email address'), null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.name}===>{self.phone_number}===>{self.email}"
