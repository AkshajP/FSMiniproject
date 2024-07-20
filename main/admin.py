from django.contrib import admin
from .models import Student,  Semester, CIE, Marks, TeacherDB

# Register your models here.
admin.site.register(Student)
admin.site.register(Semester)
admin.site.register(CIE)
admin.site.register(Marks)
admin.site.register(TeacherDB)
