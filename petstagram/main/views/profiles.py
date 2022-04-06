from django.shortcuts import render, redirect

from petstagram.main.forms import CreateProfileForm, EditProfileForm
from petstagram.main.helpers import get_profile
from petstagram.main.models import Pet, PetPhoto, Profile


def show_profile(request):
    profile = get_profile()
    pets = Pet.objects.filter(user_profile=profile)
    pet_photos = PetPhoto.objects.filter(tagged_pets__in=pets).distinct()
    # .filter(tagged_pets__user_profile = profile)
    # with distinct we get only da unique data
    total_likes_count = sum(pp.likes for pp in pet_photos)
    total_pet_photos_count = len(pet_photos)

    context = {
        'profile': profile,
        'total_likes_count': total_likes_count,
        'total_pet_photos_count': total_pet_photos_count,
    }
    return render(request, 'profile_details.html', context)


# check down the page will see function which can be reused, not writing the same code
# def create_profile(request):
#     if request.method == 'POST':
#         #create form with post
#         form = CreateProfileForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('index')
#     else:
#         #create empty form
#         form = CreateProfileForm()
#
#     context = {
#         'form': form,
#     }
#
#     return render(request, 'profile_create.html', context)
#
#
# def edit_profile(request):
#     profile = get_profile()
#     if request.method == 'POST':
#         form = EditProfileForm(request.POST, instance=profile)
#         if form.is_valid():
#             form.save()
#             return redirect('profile')
#     else:
#         form = EditProfileForm(instance=profile)
#
#     context = {
#         'form': form,
#     }
#     return render(request, 'profile_edit.html', context)


def delete_profile(request):
    return render(request, 'profile_delete.html')


# the two view actions of create and edit are almost the same, this function
# helps to better codding, organizing and reusing the same code:
def profile_action(request, form_class, success_url, instance, template_name):
    if request.method == 'POST':
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(success_url)
    else:
        form = form_class(instance=instance)

    context = {
        'form': form,
    }
    return render(request, template_name, context)


def create_profile(request):
    return profile_action(request, CreateProfileForm, 'index', Profile(), 'profile_create.html')


def edit_profile(request):
    return profile_action(request, EditProfileForm, 'profile', get_profile(), 'profile_edit.html')
