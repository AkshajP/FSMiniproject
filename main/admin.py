from django.contrib import admin
from .models import Teachers, Students, Marks, Subject

# Register your models here.
admin.site.register(Teachers)
admin.site.register(Students)
admin.site.register(Marks)
admin.site.register(Subject)
