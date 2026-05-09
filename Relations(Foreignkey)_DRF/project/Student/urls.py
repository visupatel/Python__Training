from django.urls import path
from .views import *

urlpatterns = [
    path('create-student/',create_student),
    path('create-subject/',create_subject),
    path('get-studentdata/',get_student_data),
    path('get-subject/',get_subject),
    path('update-student/',update_student),
    path('update-subject/',update_subject),
    path('delete-student/',delete_student),
    path('delete-subject/',delete_subject),
]