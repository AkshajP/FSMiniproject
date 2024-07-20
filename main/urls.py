from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),  
    path("teacher_dashboard/", views.teacher, name="teacher_dashboard"),
    path("teacher_dashboard/add_marks/", views.add_marks, name="add_marks"),
    
    
    path("teacher_dashboard/enter_marks/", views.enter_marks, name="enter_marks"),
    path("teacher_dashboard/get_marks/", views.get_marks, name="get_marks"),
    path('update_marks/<pk>/', views.update_marks, name='update_marks'),
    path("teacher_dashboard/view_marks/", views.view_marks, name="view_marks"),
    #path("teacher_dashboard/view_marks/marks2/", views.view_marks2, name="marks2"),
    path("student_dashboard/", views.student_dashboard, name="student_dashboard"),
    
    path("message_page/", views.message_page, name="message_page"),
    
]