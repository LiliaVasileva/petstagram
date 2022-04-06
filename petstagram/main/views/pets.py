from django.shortcuts import render
from petstagram.main.helpers import get_profile


def create_pet(request):
    return render(request, 'pet_create.html')


def edit_pet(request):
    return render(request, 'pet_edit.html')


def delete_pet(request):
    return render(request, 'pet_delete.html')