from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='e-home'),
    path('', views.home, name='e-about'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add-to-wishlist/<id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove-wishlist/<wishlist_item_id>/', views.remove_wishlist, name='remove_wishlist'),
]