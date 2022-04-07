from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView

from petstagram.common.view_mixins import RedirectToDashboard
from petstagram.main.models import PetPhoto
from petstagram.main.helpers import get_profile


class HomeView(RedirectToDashboard,TemplateView):
    template_name = 'home_page.html'

    # how to add context data context['hide_additional_nav_items'] = True
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hide_additional_nav_items'] = True
        return context
# This is handel now by inheriting custom created mixin RedirectToDashboard
    # # if the user is logged in should be redirect to dashbord
    # # dispatch handle the role of accessing the view
    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         return redirect('dashboard')
    #     return super().dispatch(request, *args, **kwargs)


class DashboardView(ListView):
    model = PetPhoto
    template_name = 'dashboard.html'
    # this way we named the context value to 'pet_photos' by default django use 'object_list'
    context_object_name = 'pet_photos'


# this is without any user view
# def show_dashboard(request):
#     profile = get_profile()
#     if not profile:
#         return redirect('401')
#     pet_photos = PetPhoto.objects \
#         .prefetch_related('tagged_pets') \
#         .filter(tagged_pets__user_profile=profile) \
#         .distinct()
#     context = {
#         'pet_photos': pet_photos,
#     }
#     return render(request, 'dashboard.html', context)
