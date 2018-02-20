from django.shortcuts import render, get_object_or_404
from moodleapp.decorators import teacher_required, student_required
from moodleapp.models import Teacher, Course, Student, Message
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from moodleapp.forms import CourseForm, MessageForm
from django.contrib.auth.decorators import login_required

@teacher_required
def index_teacher(request):
    courses = Course.objects.filter(prof=Teacher.objects.get(user=request.user))
    return render(request, 'moodleapp/indexteacher.html', {'courses': courses})

@student_required
def index_student(request):
    stud = Student.objects.get(user=request.user)
    return render(request, 'moodleapp/indexstudent.html', {'courses': stud.courses.all()})

@teacher_required
def add_course(request):
    course = None
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            current_user = request.user
            current_title = request.POST.get('title')
            current_description = request.POST.get('description')
            Course.objects.create(prof=Teacher.objects.get(user=current_user), title=current_title, description=current_description)
            messages.add_message(request, messages.INFO, 'Course Added!')
            return HttpResponseRedirect(reverse('moodleapp:teacher_index'))
    else:
        form = CourseForm(instance=course)
    return render(request, 'moodleapp/addcourse.html', {'form': form, 'course': course})

@student_required
def view_course(request):
    courses=Course.objects.all()
    return render(request, 'moodleapp/viewcourses.html', {'courses': courses})

@student_required()
def add_course_to_student(request, course_id):
    stud = Student.objects.get(user=request.user)
    course=Course.objects.get(id=course_id)
    stud.courses.add(course)
    return HttpResponseRedirect(reverse('moodleapp:student_index'))

@student_required()
def delete_course_from_student(request, course_id):
    stud=Student.objects.get(user=request.user)
    course=Course.objects.get(id=course_id)
    stud.courses.remove(course)
    return HttpResponseRedirect(reverse('moodleapp:student_index'))

@login_required()
def message_index(request, course_id):
    course=Course.objects.get(id=course_id)
    messages=Message.objects.filter(course=course).order_by('-timestamp')
    return render(request, 'moodleapp/indexmessage.html', {'messages': messages, 'course': course})

@teacher_required()
def add_message(request, course_id):
    message = None
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            current_label = request.POST.get('label')
            current_body = request.POST.get('body')
            Message.objects.create(course=Course.objects.get(id=course_id), label=current_label, body=current_body)
            messages.add_message(request, messages.INFO, 'Message Added!')
            return HttpResponseRedirect(reverse('moodleapp:messageindex', args=[course_id]))
    else:
        form = MessageForm(instance=message)
    return render(request, 'moodleapp/addmessage.html', {'form': form, 'message': message})
