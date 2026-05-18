from django.urls import path
from .views import *

urlpatterns = [
    path('create_book/',create_book),
    path('create_book_images/',create_book_images),
    path('create_author/',create_author),
    path("fetch_author/",fetch_author),
    path("fetch_book/",fetch_book),
    path("fetch_book_details/",fetch_book_details),
    path("update_book/",update_book),
]