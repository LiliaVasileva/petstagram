from django.contrib import admin

# по този начин регистрираме моделите в администрацията
from petstagram.accounts.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # inlines = (PetInlineAdmin,) # трябва да го добавим в тюпъл тук
    list_display = ('first_name', 'last_name')