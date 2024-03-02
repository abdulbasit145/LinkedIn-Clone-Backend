from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    """Override default method to store user by email for our Customuser."""

    def create_user(self, email, password=None, **extra_fields):
        """Create user unique by email.

        :param email: user email. must be unique.
        :param password: user's password, optional.
        :param **extra_fields: Additional fields to be set on user object.
        :return: Newly created user object.
        """
        if not email:
            raise ValueError("The given email must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create super user unique by email.

        :param email: user email. must be unique.
        :param password: user's password, optional.
        :param **extra_fields: Additional fields to be set on user object.
        :return: Newly created Super User object.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)
