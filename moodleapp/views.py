from django.shortcuts import render

def index_teacher(request):
    message='Hello, Teacher'
    return render(request, 'moodleapp/logout.html', {'message':message})

def index_student(request):
    message = 'Hello, Student'
    return render(request, 'moodleapp/logout.html', {'message':message})

