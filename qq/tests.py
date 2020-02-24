from django.test import TestCase, LiveServerTestCase
from .models import *
from django.contrib.auth import get_user_model
import time
import os
from django.conf import settings
from datetime import *


Create your tests here.

class test_course_and_lecture(TestCase):
    def setUp(self):
        user_stu = User.objects.create(username="testuser",password="webapps")
        user_pro = User.objects.create(username="professor",password="webapps")
        course = Course.objects.create(course_number="17437",course_name="web Apps",invitation_code="test")
        lecture_test = Lecture.objects.create(course = course,title = "testLecture",date = datetime.today().date())

    def test_question(self):
        c = Course.objects.get(course_number="17437")
        self.assertEqual(c.course_name,"web Apps")
        l = Lecture.objects.get(title="testLecture",course = c)
        self.assertEqual(l.title,"testLecture")


class test_question(TestCase):
    def setUp(self):
        user_stu = User.objects.create(username="testuser",password="webapps")
        user_pro = User.objects.create(username="professor",password="webapps")
        course = Course.objects.create(course_number="17437",course_name="web Apps",invitation_code="test")
        lecture_test = Lecture.objects.create(course = course,title = "testLecture",date = datetime.today().date())
        question = Question.objects.create(title="testTitle",description="description",likes = 1,lecture=lecture_test,student=user_stu)

    def test_question(self):
        q = Question.objects.get(title="testTitle")
        self.assertEqual(q.description,"description")

class test_stu_course(TestCase):
    def setUp(self):
        user_stu = User.objects.create(username="testuser",password="webapps")
        user_pro = User.objects.create(username="professor",password="webapps")
        course = Course.objects.create(course_number="17437",course_name="web Apps",invitation_code="test")
        lecture_test = Lecture.objects.create(course = course,title = "testLecture",date = datetime.today().date())
        stu_course = StudentCourse.objects.create(student = user_stu,course=course,bonus = 2)
    def test_stucourse(self):
        user_stu = User.objects.get(username="testuser")
        course = Course.objects.get(course_number="17437")
        stu_course = StudentCourse.objects.get(student=user_stu,course=course)
        self.assertEqual(stu_course.bonus,2)

class test_ans_question(TestCase):
    def setUp(self):
        user_stu = User.objects.create(username="testuser",password="webapps")
        user_pro = User.objects.create(username="professor",password="webapps")
        course = Course.objects.create(course_number="17437",course_name="web Apps",invitation_code="test")
        lecture_test = Lecture.objects.create(course = course,title = "testLecture",date = datetime.today().date())
        question = Question.objects.create(title="testTitle",description="description",likes = 1,lecture=lecture_test,student=user_stu)
        ans = Answer.objects.create(question=question,content="test_content")

    def test_ans(self):
        q = Question.objects.get(title="testTitle")
        ans = Answer.objects.filter(question=q)
        self.assertEqual(len(ans),1)