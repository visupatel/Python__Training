from django.urls import path
from .views import *

urlpatterns = [
    path("create_student/",create_student),
    path("get_student/",get_student),
    path("get_std/",get_std),
]