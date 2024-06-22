from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("student_dashboard/", views.student_dashboard, name="student_dashboard"),
    path("teacher_dashboard/",views.teacher_dashboard, name="teacher_dashboard"),
    # path("teacher_dashboard/add_marks/", views.add_marks, name="add_marks"),
    path("teacher_dashboard/edit_marks/", views.edit_marks, name="edit_marks"),
    # path("teacher_dashboard/view_marks/", views.view_marks, name="view_marks"),
]
