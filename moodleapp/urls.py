from django.urls import path
from moodleapp.views import index_teacher, index_student, add_course, view_course, add_course_to_student, delete_course_from_student, message_index, add_message,view_enrolled

app_name = 'moodleapp'

urlpatterns = [
    path('teacher/', index_teacher, name='teacher_index'),
    path('student/', index_student, name='student_index'),
    path('teacher/addcourse', add_course, name='addcourse'),
    path('student/viewcourses/', view_course, name='viewcourse'),
    path('student/add/<int:course_id>/', add_course_to_student, name='studaddcourse'),
    path('student/delete/<int:course_id>/', delete_course_from_student, name='deletecourse'),
    path('teacher/messages/<int:course_id>', message_index, name='messageindex'),
    path('teacher/messages/add/<int:course_id>/', add_message, name='add_message'),
    path('teacher/<int:course_id>/viewenrolled', view_enrolled, name='view_enrolled'),
]
