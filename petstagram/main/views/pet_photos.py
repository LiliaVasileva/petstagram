from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, DeleteView, UpdateView

from petstagram.main.models import PetPhoto


# CBV of show pet_photo details

class PetPhotoDetails(LoginRequiredMixin, DetailView):
    model = PetPhoto
    template_name = 'photo_details.html'
    context_object_name = 'pet_photo'

    # we override the get_queryset ,so we can add and prefetched_related('tagged_pets')
    # as used in the FBV bellow
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset.prefetch_related('tagged_pets')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_owner'] = self.object.user == self.request.user
        return context


class CreatePetPhotoView(LoginRequiredMixin, CreateView):
    model = PetPhoto
    template_name = 'photo_create.html'
    fields = ('photo', 'description', 'tagged_pets')
    success_url = reverse_lazy('dashboard')

    # this way we connect Pet Photo with User who created it
    def form_valid(self, form):
        # user of the instance of the form should be our user in order for the form to be valid
        form.instance.user = self.request.user
        return super().form_valid(form)


class EditPetPhotoView(UpdateView):
    model = PetPhoto
    template_name = 'photo_edit.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('pet photo details', kwargs={'pk': self.object.id})


class DeletePetPhotoView(DeleteView):
    pass


# # FBV of pet photo details:
# def show_pet_photo_details(request, pk):
#     pet_photo = PetPhoto.objects \
#         .prefetch_related('tagged_pets') \
#         .get(pk=pk)
#     context = {
#         'pet_photo': pet_photo
#     }
#     return render(request, 'photo_details.html', context)


# managing likes:
def like_pet_photo(request, pk):
    pet_photo = PetPhoto.objects.get(pk=pk)
    pet_photo.likes += 1
    pet_photo.save()
    return redirect('pet photo details', pk)


def create_pet_photo(request):
    return render(request, 'photo_create.html')


def edit_pet_photo(request):
    return render(request, 'photo_edit.html')
