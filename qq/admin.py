from django.contrib import admin

from .models import User, Student, Instructor, Course, Lecture, StudentCourse, Question, LikedQuestion, Answer

# Register your models here.
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Instructor)
admin.site.register(Course)
admin.site.register(Lecture)
admin.site.register(StudentCourse)
admin.site.register(Question)
admin.site.register(LikedQuestion)
admin.site.register(Answer)
