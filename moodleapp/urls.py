from django.urls import path
from moodleapp.views import index_teacher, index_student

app_name = 'moodleapp'

urlpatterns = [
    path('teacher/', index_teacher, name='teacher_index'),
    path('student/', index_student, name='student_index'),
]
