from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth import models as auth_models, get_user_model

# Create your models here.

# Creating custom user:
# 1. Create model extending....AbstractBaseUser, PermissionsMixin
# 2. Configure this model in settings.py = add ->AUTH_USER_MODEL = 'accounts.PetstagramUser'
# 3. Create user manager > copy code from Django UserManager

from petstagram.accounts.managers import PetstagramUserManager
from petstagram.common.validators import validate_only_letters




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


class Profile(models.Model):
    FIRST_NAME_MAX_LENGTH = 30
    FIRST_NAME_MIN_LENGTH = 2
    LAST_NAME_MAX_LENGTH = 30
    LAST_NAME_MIN_LENGTH = 2
    MALE = 'Male'
    FEMALE = 'Female'
    DO_NOT_SHOW = ' Do not show'

    GENDERS = [(x, x) for x in (MALE, FEMALE, DO_NOT_SHOW)]

    # # можем да го направим и по долният начин
    # GENDERS_OPTION_2 = [
    #     ('Male', 'Male'),
    #     ('Female', 'Female'),
    #     ('Do not show', 'Do not show'),
    # ]

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(FIRST_NAME_MIN_LENGTH),
            validate_only_letters,
        )
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
        validators=(
            MinLengthValidator(LAST_NAME_MIN_LENGTH),
            validate_only_letters,
        )
    )
    picture = models.URLField()

    # същото като горното, защото URLField наследява CharField
    # picture2 = models.CharField(
    #     validators=(
    #         URLValidator(),
    #     )
    # )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )
    description = models.TextField(
        null=True,
        blank=True,
    )

    email = models.EmailField(
        null=True,
        blank=True,
    )
    gender = models.CharField(
        max_length=max(len(x) for x, _ in GENDERS),  # динамично показваме стойност на максималната стойност
        choices=GENDERS,
        null=True,
        blank=True,
    )
    user = models.OneToOneField(
        PetstagramUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

# защо не ги оставяме да са хардкорднати, ако ни се наложи да ги използваме:
# if value == 'Male' > bad solution
# if value == Profile.MALE  => good solution
