from django.shortcuts import render

from petstagram.main.helpers import get_profile
from petstagram.main.models import Pet, PetPhoto


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


def create_profile(request):
    return render(request, 'profile_create.html')


def edit_profile(request):
    return render(request, 'profile_edit.html')


def delete_profile(request):
    return render(request, 'profile_delete.html')
