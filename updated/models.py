from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Student(models.Model):
    student = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    class_code = models.CharField(max_length=100)
    usn = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.student.first_name

class Semester(models.Model):
    sem = models.IntegerField()
    
    def __str__(self) -> str:
        return f"{self.sem}"

class CIE(models.Model):
    sem = models.ForeignKey(Semester, on_delete=models.CASCADE)
    cie = models.IntegerField()
    sub_code = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return f"{self.cie}"
    
class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    cie = models.ForeignKey(CIE, on_delete=models.CASCADE)
    marks = models.IntegerField(null=True)
    attendance = models.CharField(max_length=50, null=True)
    
    def __str__(self) -> str:
        return f"{self.marks}"
    
class TeacherDB(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    
    def __str__(self):
        return self.name