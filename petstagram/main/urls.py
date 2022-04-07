from django.urls import path

from petstagram.main.views.generic import HomeView, DashboardView
from petstagram.main.views.pet_photos import  edit_pet_photo, like_pet_photo, \
    PetPhotoDetails, CreatePetPhotoView
from petstagram.main.views.pets import CreatePetView, EditPetView, DeletePetView
from petstagram.main.views.profiles import create_profile, edit_profile, delete_profile, \
    ProfileDetailsViews

urlpatterns = [
    # generic views
    path('', HomeView.as_view(), name='index'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # profile views
    path('profile/<int:pk>/', ProfileDetailsViews.as_view(), name='profile'),
    path('profile/create/', create_profile, name='profile create'),
    path('profile/edit/', edit_profile, name='profile edit'),
    path('profile/delete/', delete_profile, name='profile delete'),
    # photo views
    path('photo/add/', CreatePetPhotoView.as_view(), name='pet photo create'),
    path('photo/edit/<int:pk>', edit_pet_photo, name='pet photo edit'),
    path('photo/details/<int:pk>', PetPhotoDetails.as_view(), name='pet photo details'),
    path('photo/like/<int:pk>', like_pet_photo, name='like pet photo'),
    # pet views
    path('pet/create/', CreatePetView.as_view(), name='pet create'),
    path('pet/edit/<int:pk>', EditPetView.as_view(), name='pet edit'),
    path('pet/delete/<int:pk>', DeletePetView.as_view(), name='pet delete'),
]
