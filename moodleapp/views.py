from django.shortcuts import render, get_object_or_404
from moodleapp.decorators import teacher_required, student_required
from moodleapp.models import Teacher, Course, Student, Message, Enrollment
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from moodleapp.forms import CourseForm, MessageForm

@teacher_required
def index_teacher(request):
    courses = Course.objects.filter(prof=Teacher.objects.get(user=request.user))
    return render(request, 'moodleapp/indexteacher.html', {'courses': courses})

@student_required
def index_student(request):
    stud = Student.objects.get(user=request.user)
    enrollments=Enrollment.objects.filter(student=stud)
    course_list=[]
    for enrollment in enrollments:
        course_list.append(enrollment.course)
    return render(request, 'moodleapp/indexstudent.html', {'courses': course_list})

@teacher_required
def add_course(request):
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
        form = CourseForm()
    return render(request, 'moodleapp/addcourse.html', {'form': form})

@student_required
def view_course(request):
    stud = Student.objects.get(user=request.user)
    enrollments = Enrollment.objects.filter(student=stud);
    course_list = []
    for enrollment in enrollments:
        course_list.append(enrollment.course)
    courses=Course.objects.exclude(id__in=[o.id for o in course_list])
    return render(request, 'moodleapp/viewcourses.html', {'courses': courses})

@student_required()
def add_course_to_student(request, course_id):
    stud = Student.objects.get(user=request.user)
    course=Course.objects.get(id=course_id)
    Enrollment.objects.create(student=stud, course=course)
    return HttpResponseRedirect(reverse('moodleapp:student_index'))

@student_required()
def delete_course_from_student(request, course_id):
    stud=Student.objects.get(user=request.user)
    course=Course.objects.get(id=course_id)
    Enrollment.objects.get(student=stud, course=course).delete()
    return HttpResponseRedirect(reverse('moodleapp:student_index'))

@teacher_required()
def teacher_message_index(request, course_id):
    course=Course.objects.get(id=course_id)
    messages=Message.objects.filter(course=course).order_by('-timestamp')
    return render(request, 'moodleapp/indexmessage.html', {'messages': messages, 'course': course})

@student_required()
def student_message_index(request, course_id):
    stud = Student.objects.get(user=request.user)
    course = Course.objects.get(id=course_id)
    enrollment=Enrollment.objects.get(student=stud, course=course)
    messages = Message.objects.filter(course=course, timestamp__gt=enrollment.timestamp)
    return render(request, 'moodleapp/indexmessage.html', {'messages': messages, 'course': course})

@teacher_required()
def add_message(request, course_id):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            current_label = request.POST.get('label')
            current_body = request.POST.get('body')
            Message.objects.create(course=Course.objects.get(id=course_id), label=current_label, body=current_body)
            messages.add_message(request, messages.INFO, 'Message Added!')
            return HttpResponseRedirect(reverse('moodleapp:teachermessageindex', args=[course_id]))
    else:
        form = MessageForm()
    return render(request, 'moodleapp/addmessage.html', {'form': form})

@teacher_required()
def view_enrolled(request, course_id):
    course=Course.objects.get(id=course_id)
    enrollments=Enrollment.objects.filter(course=course)
    student_list=[]
    for enrollment in enrollments:
        student_list.append(enrollment.student)
    return render(request, 'moodleapp/viewenrolled.html', {'students': student_list})

@teacher_required()
def delete_message(request, course_id, message_id):
    Message.objects.get(id=message_id).delete()
    return HttpResponseRedirect(reverse('moodleapp:teachermessageindex', args=[course_id]))
