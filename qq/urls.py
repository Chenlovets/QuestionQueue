from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('main', views.enter_queue, name='main'),
    path('student_courses', views.student_courses, name='student_courses'),
    path('professor_courses', views.professor_courses, name='professor_courses'),
    path('ta_courses', views.ta_courses, name='ta_courses'),
    path('answers', views.answers, name='answers'),
    path('postQuestion',views.post_question, name='post_question'),
    path('likeTheQ',views.like,name='like'),
    path('dislikeTheQ',views.dislike,name="dislike"),
    path('getQuestion',views.get_question,name='get_question'),
    path('getAnswers',views.get_answers,name='get_answers'),
    path('add_new_course',views.add_new_course,name='add_new_course'),
    path('join_existing_course',views.join_existing_course,name='join_existing_course'),
    path('ta_join_existing_course',views.ta_join_existing_course,name='ta_join_existing_course'),
    path('delete_course',views.delete_course,name='delete_course'),
    path('enter_new_queue', views.enter_new_queue, name='enter_new_queue'),
    path('exit_course', views.exit_course, name='exit_course'),
    path('professor_lecture',views.professor_lecture,name='professor_lecture'),
    path('add_new_lecture',views.add_new_lecture,name='add_new_lecture'),
    path('submitAnswer',views.submitAnswer,name="submitAnswer"),
    path('delete_lecrture',views.delete_lecture,name='delete_lecture'),
    path('get_my_question/<int:course_id>/',views.get_my_question,name='get_my_question'),
    path('get_liked_question/<int:course_id>/',views.get_liked_question,name='get_liked_question'),
    path('my_questions/<int:course_id>/', views.my_questions, name='my_questions'),
    path('enter_queue',views.enter_queue,name="enter_queue"),
    path('enter_leaderboard',views.enter_leaderboard,name="enter_leaderboard"),
    path('get_leaderboard_stu',views.get_leaderboard_stu,name="get_leaderboard_stu"),
    path('deleteQuestion',views.deleteQuestion,name="deleteQuestion"),
    path('redirect_after_login',views.redirect_after_login, name="redirect_after_login"),
    url(r'^accounts/', include('allauth.urls')),

]
