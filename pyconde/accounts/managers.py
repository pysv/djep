from django.contrib.auth import get_user_model
from django.contrib.auth.models import BaseUserManager
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email, password=password, is_staff=True, is_superuser=True,
            **extra_fields)
        return user

    def create_inactive_user(self, email, **extra_fields):
        """Create a new inactive user without password"""
        return self.create_user(email=email, password=None, is_active=False, **extra_fields)

    def get_by_uidb64(self, uidb64):
        """
        Return user object if base64 encoded uid matching one else None.
        """
        try:
            # urlsafe_base64_decode() decodes to bytestring on Python 3
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = self.get(pk=uid)
        except (TypeError, ValueError, OverflowError, get_user_model().DoesNotExist):
            user = None
        return user
