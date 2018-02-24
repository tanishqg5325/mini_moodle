from django.urls import path
from . import views

app_name = 'moodleapp'

urlpatterns = [
    path('teacher/', views.index_teacher, name='teacher_index'),
    path('student/', views.index_student, name='student_index'),
    path('teacher/addcourse', views.add_course, name='addcourse'),
    path('student/viewcourses/', views.view_course, name='viewcourse'),
    path('student/add/<int:course_id>/', views.add_course_to_student, name='studaddcourse'),
    path('student/delete/<int:course_id>/', views.delete_course_from_student, name='deletecourse'),
    path('teacher/<int:course_id>/messages/', views.teacher_message_index, name='teachermessageindex'),
    path('student/<int:course_id>/messages/', views.student_message_index, name='studentmessageindex'),
    path('teacher/messages/add/<int:course_id>/', views.add_message, name='add_message'),
    path('teacher/<int:course_id>/viewenrolled', views.view_enrolled, name='view_enrolled'),
    path('teacher/<int:course_id>/<int:message_id>/delete/', views.delete_message, name='deletemessage'),
]
