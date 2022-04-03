import datetime

from django.core.validators import MinLengthValidator, URLValidator
from django.db import models

from petstagram.main.validators import validate_only_letters, validate_file_max_size_in_mb


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
    def __str__(self):
        return f'{self.first_name} {self.last_name}'


# защо не ги оставяме да са хардкорднати, ако ни се наложи да ги използваме:
# if value == 'Male' > bad solution
# if value == Profile.MALE  => good solution

class Pet(models.Model):
    #Constants
    NAME_MAX_LENGTH = 30
    CAT = 'Cat'
    DOG = 'Dog'
    BUNNY = 'Bunny'
    PARROT = 'Parrot'
    FISH = 'Fish'
    OTHER = 'Other'
    TYPES = [(x, x) for x in (CAT, DOG, FISH, PARROT, BUNNY, OTHER)]

    #Fields/Columns
    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
    )
    type = models.CharField(
        max_length=max(len(x) for (x, _) in TYPES),
        choices=TYPES,
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )
    # One to one relations

    # One to many relations
    user_profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
    )
    # Many to many relations

    # Other proparties , methods,  dunder methods

    #изчисляване на  възрастта на Pet-a
    @property
    def age(self):
        return datetime.datetime.now().year - self.date_of_birth.year

    # Meta uniques info данни за самата таблица,
    class Meta:
        unique_together = ('user_profile', 'name')
        # прави тези двете да са уникална двойка


class PetPhoto(models.Model):
    photo = models.ImageField()
    #     validators=(
    #         validate_file_max_size_in_mb(5),
    #     )
    # )
    tagged_pets = models.ManyToManyField(
        Pet,
        # validate at least 1 pet
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    publication_date = models.DateTimeField(
        auto_now_add=True,
    )
    likes = models.IntegerField(
        default=0,
    )