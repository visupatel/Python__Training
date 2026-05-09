from django.urls import path
from .views import *



urlpatterns = [
    path('create_student/', create_student),
    path('create_student_profile/', create_student_profile),
    path("get_student/",get_student),
    path("get_student_profile/",get_student_profile),
    path('update_student/',update_student),
    path('update_student_profile/',update_student_profile),
    path('delete_student/',delete_student),
    
]
