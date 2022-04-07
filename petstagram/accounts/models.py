from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import models as auth_models

# Create your models here.

# Creating custom user:
# 1. Create model extending....AbstractBaseUser, PermissionsMixin
# 2. Configure this model in settings.py = add ->AUTH_USER_MODEL = 'accounts.PetstagramUser'
# 3. Create user manager > copy code from Django UserManager

from petstagram.accounts.managers import PetstagramUserManager


class PetstagramUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    USERNAME_MAX_LEN = 25
    username = models.CharField(
        max_length=USERNAME_MAX_LEN,
        unique=True,
    )
    # need to have
    USERNAME_FIELD = 'username'
    # nice to have
    date_joined = models.DateTimeField(
        auto_now_add=True,
    )
    # nice to have so we can use it via admin
    is_staff = models.BooleanField(
        default=False,
    )

    object = PetstagramUserManager()
