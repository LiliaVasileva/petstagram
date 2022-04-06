from django.urls import path

from petstagram.main.views.generic import show_home, show_dashboard
from petstagram.main.views.pet_photos import create_pet_photo, edit_pet_photo, like_pet_photo, show_pet_photo_details
from petstagram.main.views.pets import create_pet, edit_pet, delete_pet
from petstagram.main.views.profiles import show_profile, create_profile, edit_profile, delete_profile

urlpatterns = [
    #generic views
    path('', show_home, name='index'),
    path('dashboard/' ,show_dashboard, name='dashboard'),
    #profile views
    path('profile/', show_profile, name='profile'),
    path('profile/create/', create_profile, name = 'profile create'),
    path('profile/edit/', edit_profile, name = 'profile edit'),
    path('profile/delete/', delete_profile, name = 'profile delete'),
    #photo views
    path('photo/add/,', create_pet_photo, name='pet photo create'),
    path('photo/edit/<int:pk>', edit_pet_photo, name='pet photo edit'),
    path('photo/details/<int:pk>', show_pet_photo_details, name='pet photo details'),
    path('photo/like/<int:pk>',like_pet_photo,name='like pet photo'),
    #pet views
    path('pet/create/', create_pet, name= 'pet create'),
    path('pet/edit/<int:pk>', edit_pet, name= 'pet edit'),
    path('pet/delete/<int:pk>', delete_pet, name= 'pet delete'),
    ]

