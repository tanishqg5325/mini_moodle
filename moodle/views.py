from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from moodleapp.forms import StudentSignUpForm, TeacherSignUpForm
from moodleapp.models import User
from django.views.generic import (CreateView, DeleteView, DetailView, ListView, UpdateView, TemplateView)


def conf(request):
    if request.user.is_teacher:
        return redirect('moodleapp:teacher_index')
    else:
        return redirect('moodleapp:student_index')

class SignUpView(TemplateView):
    template_name = 'moodleapp/signup.html'

class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'moodleapp/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('moodleapp:student_index')

class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'moodleapp/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('moodleapp:teacher_index')

