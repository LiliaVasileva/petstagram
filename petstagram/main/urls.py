from django.urls import path

from petstagram.main.views.generic import HomeView, DashboardView
from petstagram.main.views.pet_photos import edit_pet_photo, like_pet_photo, \
    PetPhotoDetails, CreatePetPhotoView, DeletePetPhotoView, EditPetPhotoView
from petstagram.main.views.pets import CreatePetView, EditPetView, DeletePetView

urlpatterns = [
    # generic views
    path('', HomeView.as_view(), name='index'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # photo views
    path('photo/add/', CreatePetPhotoView.as_view(), name='pet photo create'),
    path('photo/edit/<int:pk>', EditPetPhotoView.as_view(), name='pet photo edit'),
    path('photo/details/<int:pk>', PetPhotoDetails.as_view(), name='pet photo details'),
    path('photo/like/<int:pk>', like_pet_photo, name='like pet photo'),
    path('photo/delete/<int:pk>', DeletePetPhotoView.as_view(), name='pet photo delete'),
    # pet views
    path('pet/create/', CreatePetView.as_view(), name='pet create'),
    path('pet/edit/<int:pk>', EditPetView.as_view(), name='pet edit'),
    path('pet/delete/<int:pk>', DeletePetView.as_view(), name='pet delete'),
]
