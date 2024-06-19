# from django.db import models

# # class Teacher(models.Model):
# #     name = models.CharField(max_length=100)
# #     email = models.EmailField(unique=True)
# #     password = models.CharField(max_length=100)  

# #     def __str__(self):
# #         return self.name

# class Student(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     usn = models.CharField(max_length=50, unique=True)
#     subjects = models.ManyToManyField('Subject', through='Marks')

#     def __str__(self):
#         return self.name

# class Subject(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name

# class Marks(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
#     marks = models.IntegerField()

#     class Meta:
#         unique_together = ('student', 'subject')

# class TeacherDB(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.EmailField(max_length=254)
    
#     def __str__(self):
#         return self.email
    


