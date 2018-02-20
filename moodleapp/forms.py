from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from moodleapp.models import  User, Teacher, Student, Course
from django import forms

class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_teacher = True
        user.save()
        Teacher.objects.create(user=user)
        return user

class StudentSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        Student.objects.create(user=user)
        return user

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title', 'description')

