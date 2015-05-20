from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyUserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        """
        Creates and saves a User with the given email, username
        and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        """
        Creates and saves a superuser with the given email, username
        and password.
        """
        user = self.create_user(
            username,
            password=password,
            email=self.normalize_email(email),

        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    """Custom User"""
    username = models.CharField(max_length=30, blank=False, unique=True)
    email = models.EmailField(max_length=30, blank=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = MyUserManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        # The user is identified by their email address
        return self.username

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Author(models.Model):
    google_uid = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=30)
    avatar_url = models.URLField(max_length=200)
    user = models.OneToOneField(User, null=True)
