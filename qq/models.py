from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class User(AbstractUser):

	andrewID = models.CharField(max_length=10)
	is_instructor = models.BooleanField(default = False)
	is_student = models.BooleanField(default = True)
	
	def __str__(self):
		return str(self.andrewID)

class Student(models.Model):

	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
	
	def __str__(self):
		return str(self.user.andrewID)

class Instructor(models.Model):

	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='instructor_profile')

	def __str__(self):
		return str(self.user.andrewID)

class Course(models.Model):

	course_number = models.CharField(max_length = 30)
	course_name = models.CharField(max_length = 100)
	students = models.ManyToManyField(User, blank=True, related_name="students")
	instructors = models.ManyToManyField(User, related_name="instructors")
	invitation_code = models.CharField(max_length=30)

	def __str__(self):
		return str(self.course_number)

class Lecture(models.Model):

	course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course')
	title = models.CharField(max_length=100)
	date = models.DateField(auto_now = True)

	def __str__(self):
		return str(self.title)

class StudentCourse(models.Model):

	student = models.ForeignKey(User, on_delete = models.CASCADE,related_name="student_bonus")
	course = models.ForeignKey(Course, on_delete = models.CASCADE,related_name="course_bonus")
	bonus = models.PositiveIntegerField(default = 0)

	def __str__(self):
		return str(self.pk)

class Question(models.Model):

	title = models.CharField(max_length=100)
	description = models.CharField(max_length=1000)
	likes = models.IntegerField(default=1)
	lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, related_name='lecture')
	student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student')

	def __str__(self):
		return str(self.pk)

class LikedQuestion(models.Model):

	student = models.ForeignKey(User, on_delete = models.CASCADE)
	question = models.ForeignKey(Question, on_delete = models.CASCADE)

	def __str__(self):
		return str(self.pk)

class Answer(models.Model):

	content = models.CharField(max_length = 1000)
	question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question')

	def __str__(self):
		return str(self.pk)


