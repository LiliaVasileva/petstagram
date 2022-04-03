from django.contrib import admin

# Register your models here.
from petstagram.main.models import Profile, Pet, PetPhoto

# клас, който ни създава в навигацията форма в самият профил за създаване на Pet
class PetInlineAdmin(admin.StackedInline):
    model = Pet

# по този начин регистрираме моделите в администрацията
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    inlines = (PetInlineAdmin,) # трябва да го добавим в тюпъл тук
    list_display = ('first_name',  'last_name')


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')


@admin.register(PetPhoto)
class PetPhotoAdmin(admin.ModelAdmin):
    pass
