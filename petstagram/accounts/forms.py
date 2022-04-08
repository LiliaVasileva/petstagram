from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from petstagram.accounts.models import Profile
from petstagram.common.form_mixins import BootstrapFormMixin
from petstagram.main.models import PetPhoto


class CreateProfileForm(BootstrapFormMixin, UserCreationForm):
    first_name = forms.CharField(
        max_length=Profile.FIRST_NAME_MAX_LENGTH,
    )
    last_name = forms.CharField(
        max_length=Profile.LAST_NAME_MAX_LENGTH
    )
    picture = forms.URLField()
    date_of_birth = forms.DateField()
    description = forms.CharField(
        widget=forms.Textarea,
    )
    email = forms.EmailField()
    gender = forms.ChoiceField(
        choices=Profile.GENDERS,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    def save(self, commit=True):
        user = super().save(commit=True)
        # if the fields match we can use cleaned_data
        # profile= Profile(
        #     **self.cleaned_data,
        #     user=user
        # )
        # if the fields don't match we need to type them one by one
        profile = Profile(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            picture=self.cleaned_data['picture'],
            date_of_birth=self.cleaned_data['date_of_birth'],
            description=self.cleaned_data['description'],
            email=self.cleaned_data['email'],
            gender=self.cleaned_data['gender'],
            user=user,
        )

        if commit:
            profile.save()

        return user

    class Meta:
        model = get_user_model()
        # we should choose one from the two options fields or exclude
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'picture', 'description', 'gender',
                  'email', 'date_of_birth']
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
