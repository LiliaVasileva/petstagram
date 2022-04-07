import datetime
from datetime import date

from django import forms
from django.core.exceptions import ValidationError

from petstagram.main.models import Profile, PetPhoto, Pet


# Easier way to fix the visualization of the fields in form
# creating mixin, to be inherited by the ProfileForm class
class BootstrapFormMixin:
    fields = {}

    def _init_bootstrap_form_controls(self):
        for _, field in self.fields.items():
            if not hasattr(field.widget, 'attrs'):
                setattr(field.widget, 'attrs', {})
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = ''
            field.widget.attrs['class'] += 'form-control'


class DisabledFieldsFormMixin:
    # when we inherit this class we can disable all or only some fields if we add disabled fields = ('name')
    # in the child class this will disable only filed = name
    disabled_fields = '__all__'
    fields = {}

    def _init_disabled_fields(self):
        for name, field in self.fields.items():
            if self.disabled_fields != '__all__' and name not in self.disabled_fields:
                continue
            if not hasattr(field.widget, 'attrs'):
                setattr(field.widget, 'attrs', {})
            field.widget.attrs['readonly'] = 'readonly'


class CreateProfileForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = Profile
        # we should choose one from the two options fields or exclude
        fields = ['first_name', 'last_name', 'picture']
        # html controls which needs to be visualized widgets,
        #  with widgets we fix the visualization of the form in the html page
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    # adding 'class' : 'form-control' - is anather way of handeling the form visualization
                    # 'class': 'form-control',
                    'placeholder': 'Enter first name',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    # 'class': 'form-control',
                    'placeholder': 'Enter last name'
                }
            ),
            'picture': forms.TextInput(
                attrs={
                    # 'class': 'form-control',
                    'placeholder': 'Enter URL'
                }
            ),
        }


class EditProfileForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()
        # setting default value to a choice fild in the form -> self.initial['choice field name'] = wanted_value
        self.initial['gender'] = Profile.DO_NOT_SHOW

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'picture', 'date_of_birth', 'email', 'gender', 'description']  # /'__all__'

        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter first name',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter last name'
                },
            ),
            'picture': forms.TextInput(
                attrs={
                    'placeholder': 'Enter URL'
                },
            ),
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'Enter email'
                }
            ),
            'gender': forms.Select(
                choices=Profile.GENDERS,

            ),
            'description': forms.Textarea(
                attrs={
                    'placeholder': 'Enter description',
                    'rows': 3,
                }
            ),
            'date_of_birth': forms.DateInput(
                attrs={
                    'min': '1920-01-01',
                }
            )
        }


class DeleteProfileForm(forms.ModelForm):

    def save(self, commit=True):
        # we need to delete all photos with tagged pets from this profile, when deleting the profile
        pets = list(self.instance.pet_set.all())
        pet_photos = PetPhoto.objects.filter(tagged_pets__in=pets)
        pet_photos.delete()
        self.instance.delete()
        return self.instance

    class Meta:
        model = Profile
        exclude = ['first_name', 'last_name', 'picture', 'date_of_birth', 'email', 'gender', 'description']


class CreatePetForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        pet = super().save(commit=False)
        pet.user = self.user

        if commit:
            pet.save()
        return pet

    class Meta:
        model = Pet
        fields = ['name', 'type', 'date_of_birth']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'Enter pet name',
                }
            ),
        }


class EditPetForm(forms.ModelForm, BootstrapFormMixin):
    MIN_DATE_OF_BIRTH = date(1920, 1, 1)
    MAX_DATE_OF_BIRTH = date.today()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data['date_of_birth']
        if date_of_birth < self.MIN_DATE_OF_BIRTH or self.MAX_DATE_OF_BIRTH < date_of_birth:
            raise ValidationError(
                f'Date of birth must be between {self.MIN_DATE_OF_BIRTH} and {self.MAX_DATE_OF_BIRTH}')
        return date_of_birth

    class Meta:
        model = Pet
        exclude = ['user_profile']


class DeletePetForm(forms.ModelForm, BootstrapFormMixin, DisabledFieldsFormMixin):

    # disabled_fields = ('name') explain in the DisabledFieldsFormMixin comments

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()
        self._init_disabled_fields()

    def save(self, commit=True):
        self.instance.delete()
        return self.instance

    class Meta:
        model = Pet
        exclude = ['user_profile']
