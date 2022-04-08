from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from petstagram.main.forms import CreatePetForm, EditPetForm, DeletePetForm


# Class Base Views:

class CreatePetView(CreateView):
    form_class = CreatePetForm
    template_name = 'pet_create.html'
    success_url = reverse_lazy('dashboard')

    # this way we define the pet to be created for the currant user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class EditPetView(UpdateView):
    form_class = EditPetForm
    template_name = 'pet_edit.html'


class DeletePetView(DeleteView):
    form_class = DeletePetForm
    template_name = 'pet_delete.html'

# function base views:
# def pet_action(request, form_class, success_url, instance, template_name):
#     if request.method == 'POST':
#         form = form_class(request.POST, instance=instance)
#         if form.is_valid():
#             form.save()
#             return redirect(success_url)
#     else:
#         form = form_class(instance=instance)
#
#     context = {
#         'form': form,
#         'pet': instance,
#     }
#     return render(request, template_name, context)
#
#
# def create_pet(request):
#     return pet_action(request, CreatePetForm, 'profile', Pet(user_profile=get_profile()), 'pet_create.html')
#
#
# def edit_pet(request, pk):
#     return pet_action(request, EditPetForm, 'profile', Pet.objects.get(pk=pk), 'pet_edit.html')
#
#
# def delete_pet(request, pk):
#     return pet_action(request, DeletePetForm, 'profile', Pet.objects.get(pk=pk), 'pet_delete.html')
