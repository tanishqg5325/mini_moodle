from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_student = models.BooleanField('student status', default=False)
    is_teacher = models.BooleanField('teacher status', default=False)

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username

class Course(models.Model):
    prof = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    description = models.TextField()

    def __str__(self):
        return self.title

class Message(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    label = models.CharField(max_length=200)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.label

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    courses = models.ManyToManyField(Course)

    def __str__(self):
        return self.user.username
