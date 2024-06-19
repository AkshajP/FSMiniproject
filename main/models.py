from django.db import models

# Create your models here.

class Teachers(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)    
    
    def __str__(self):
        return self.name
    
class Students(models.Model):
    usn = models.CharField(max_length = 10)    
    name = models.CharField(max_length = 100)
    email = models.EmailField(max_length=254)
    counsellor = models.ForeignKey(Teachers, on_delete=models.CASCADE, related_name="counsellor")
    
    def __str__(self):
        return self.name
    
class Subject(models.Model):
    sem = models.IntegerField()
    sub_code = models.CharField(max_length=15)
    sub_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.sub_name
    
class Marks(models.Model):
    sub_code = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="subject_code")
    cie = models.IntegerField()
    usn = models.ForeignKey(Students, on_delete=models.CASCADE, related_name="student_usn")
    marks = models.DecimalField(max_digits=4, decimal_places=2)
    attendance = models.CharField(max_length=10)
    
    def __str__(self):
        return self.usn