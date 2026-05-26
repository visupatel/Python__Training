from django.urls import path
from .views import *

urlpatterns = [
    path('author/',AuthorView.as_view()),
    path('book/',BookView.as_view()),
    path('bookImages/',BookImageView.as_view()),
    path('authors/',AuthorViewSerializer.as_view()),
    path('books/',BookViewSerializer.as_view()),
    path('booksImg/',BookImageViewSerializer.as_view()),
    path('details/',AuthorBookView.as_view()),
    path('optimiz_author/',OptimizeAuthor.as_view()),
    path('fetch/',FetchData.as_view()),
]