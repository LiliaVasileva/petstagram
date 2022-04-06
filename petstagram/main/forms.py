from django import forms

from petstagram.main.models import Profile


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
                    #'class': 'form-control',
                    'placeholder': 'Enter last name'
                }
            ),
            'picture': forms.TextInput(
                attrs={
                    #'class': 'form-control',
                    'placeholder': 'Enter URL'
                }
            ),
        }


class EditProfileForm(BootstrapFormMixin,forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()
        # setting default value to a choice fild in the form -> self.initial['choice field name'] = wanted_value
        self.initial['gender'] = Profile.DO_NOT_SHOW

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'picture', 'date_of_birth', 'email', 'gender', 'description'] # /'__all__'

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