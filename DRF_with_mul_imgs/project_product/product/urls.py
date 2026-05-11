from django.urls import path
from .views import *


urlpatterns = [
    path('create_prod/',create_prod),
    path('create_prod_img/',create_prod_img),
    path('get_img/',get_img),
    path('update_product/',update_product),
    path('update_prod_images/',update_prod_images),
    path('delete_product/', delete_product),
    path('search/', search),
]