from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy


class UserRegisterView:
    pass


class UserLoginView(LoginView):
    template_name = 'accounts/login_page.html'
    success_url = reverse_lazy('dashboard')

    # if success_url is aplaid
    def get_success_url(self):
        if self.success_url:
            return self.success_url
        return super().get_success_url()



class UserDetailsView:
    pass


class EditProfileView:
    pass


class ChangeUserPasswordView:
    pass
