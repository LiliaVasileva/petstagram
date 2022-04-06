from django.shortcuts import render, redirect

from petstagram.main.models import Profile, PetPhoto, Pet


def get_profile():
    profile = Profile.objects.all()
    if profile:
        return profile[0]
    return None


def show_home(request):
    context = {
        'hide_additional_nav_items': True,
    }

    return render(request, 'home_page.html', context)


def show_dashboard(request):
    profile = get_profile()
    if not profile:
        return redirect('401')
    pet_photos = PetPhoto.objects \
        .prefetch_related('tagged_pets') \
        .filter(tagged_pets__user_profile=profile) \
        .distinct()
    context = {
        'pet_photos': pet_photos,
    }
    return render(request, 'dashboard.html', context)


def show_profile(request):
    profile = get_profile()
    pets = Pet.objects.filter(user_profile= profile)
    pet_photos = PetPhoto.objects.filter(tagged_pets__in=pets).distinct()
    #.filter(tagged_pets__user_profile = profile)
    # with distinct we get only da unique data
    total_likes_count = sum(pp.likes for pp in pet_photos)
    total_pet_photos_count = len(pet_photos)

    context = {
        'profile': profile,
        'total_likes_count': total_likes_count,
        'total_pet_photos_count': total_pet_photos_count,
    }
    return render(request, 'profile_details.html', context)


def show_pet_photo_details(request, pk):
    pet_photo = PetPhoto.objects \
        .prefetch_related('tagged_pets') \
        .get(pk=pk)
    context = {
        'pet_photo': pet_photo
    }
    return render(request, 'photo_details.html', context)


# managing likes:
def like_pet_photo(request, pk):
    pet_photo = PetPhoto.objects.get(pk=pk)
    pet_photo.likes += 1
    pet_photo.save()
    return redirect('pet photo details', pk)
