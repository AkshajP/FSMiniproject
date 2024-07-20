from django.urls import path
from . import views

urlpatterns = [
    path("teacher_register/", views.teacher_register, name="teacher_register"),
    path("student_register/", views.student_register, name="student_register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
]
