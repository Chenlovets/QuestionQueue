from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .decorators import instructor_required, student_required, student_or_instructor_required, ta_required,ta_or_instructor_required
from django.contrib.auth import login, authenticate, get_user_model, views
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core import serializers
from django.db.models import Max
from django.urls import reverse
from .models import *
from .forms import *
from qq import views
from datetime import *
import json
import re


# Create your views here.

def index(request):
    return render(request, 'qq/index.html')

@student_or_instructor_required
def redirect_after_login(request):
    if request.user.is_authenticated:
        # login users are students at default, so check the email address
        if request.user.is_student:
            # if student email (match keyword andrew)
            if re.match('.*andrew.cmu.edu$', request.user.email):
                return redirect('student_courses')
            # if not student email (no keyward andrew)
            if re.match('.*cmu.edu$', request.user.email):
                request.user.is_student = False
                request.user.is_instructor = True
                request.user.save()
                return redirect('professor_courses')
        elif request.user.is_instructor:
            return redirect('professor_courses')
    else:
        return redirect('index')
    
# Student End

@student_required
def main(request):
    question_items = Question.objects.order_by('-likes')
    return render(request, 'qq/main.html', {'questions': question_items})

@student_required
def enter_queue(request):
    if request.method == "POST":
        if "course_id" in request.POST:
            course_id = request.POST["course_id"]
            lecture_id = Lecture.objects.filter(course_id=course_id).aggregate(Max('id'))['id__max']
            question_items = Question.objects.filter(lecture_id=lecture_id).order_by('-likes')

            questions = []
            for question in question_items:
                
                # identify if the question is liked by the user
                is_liked = False
                like_questions = LikedQuestion.objects.filter(student=request.user).filter(question=question)
                like_question = None
                for l in like_questions:
                    like_question = l
                if like_question != None:
                    is_liked = True

                # add answers
                answers = Answer.objects.filter(question=question)
                answers_str = []
                count = 1
                for ans in answers:
                    answers_display = '<li class="list-group-item">Answer'
                    answers_display += str(count)
                    answers_display += ' : '
                    answers_display += ans.content
                    answers_display += '</li>'
                    count = count + 1
                    answers_str.append(answers_display)

                questions.append({"id":question.id,'title':question.title,"description":question.description,
                             "likes":question.likes,"is_liked":is_liked, "answers":answers_str})
            
        return render(request, 'qq/main.html', {'questions': questions, "lecture_id": lecture_id, "course_id": course_id})
    return index(request)

@student_required
def get_question(request):
    if request.method == "GET":
        if "lecture_id" in request.GET:
            lecture_id = request.GET["lecture_id"]
            questions = Question.objects.filter(lecture_id=lecture_id).order_by('-likes')
            json = []
            for question in questions:
                is_liked = False
                # identify if the question is liked by the user
                like_questions = LikedQuestion.objects.filter(student=request.user).filter(question=question)
                like_question = None
                for l in like_questions:
                    like_question = l
                if like_question != None:
                    is_liked = True
                # add answers
                answers = Answer.objects.filter(question=question)
                answers_str = []
                count = 1
                for ans in answers:
                    answers_display = '<li class="list-group-item">Answer'
                    answers_display += str(count)
                    answers_display += ' : '
                    answers_display += ans.content
                    answers_display += '</li>'
                    count = count + 1
                    answers_str.append(answers_display)

                json.append({"id":question.id,'title':question.title,"description":question.description,
                             "likes":question.likes,"is_liked":is_liked, "answers":answers_str})

            return JsonResponse({'questions':list(json)})
    
    return index(request)

@student_required
def post_question(request):
    if request.method == "POST":
        if 'title' in request.POST and 'content' in request.POST and 'lecture_id' in request.POST and "course_id" in request.POST:
            title = request.POST['title']
            content = request.POST['content']
            lecture_id = request.POST['lecture_id']
            course_id = request.POST["course_id"]
            student = request.user
            if not re.match(r"\s+", content) and not re.match(r"\s+", title):
                q = Question(title=title, description=content, lecture_id=lecture_id, student=student, likes=0)
                q.save()
            question_items = Question.objects.filter(lecture_id=lecture_id).order_by('-likes')
            questions = []
            for question in question_items:
                
                # identify if the question is liked by the user
                is_liked = False
                like_questions = LikedQuestion.objects.filter(student=request.user).filter(question=question)
                like_question = None
                for l in like_questions:
                    like_question = l
                if like_question != None:
                    is_liked = True

                # add answers
                answers = Answer.objects.filter(question=question)
                answers_str = []
                count = 1
                for ans in answers:
                    answers_display = '<li class="list-group-item">Answer'
                    answers_display += str(count)
                    answers_display += ' : '
                    answers_display += ans.content
                    answers_display += '</li>'
                    count = count + 1
                    answers_str.append(answers_display)

                questions.append({"id":question.id,'title':question.title,"description":question.description,
                             "likes":question.likes,"is_liked":is_liked, "answers":answers_str})


    return render(request, 'qq/main.html', {'questions': questions, "lecture_id": lecture_id, "course_id": course_id})


@student_required
def like(request):
    if request.method == 'POST':
        if request.is_ajax():
            if "questionID" in request.POST:
                id = request.POST["questionID"]
                q = Question.objects.get(id=id)
                count = LikedQuestion.objects.filter(student=request.user,question=q).count()
                if (count == 0):
                    likes_number = q.likes
                    likes_number += 1
                    q.likes = likes_number
                    q.save()
                    LikedQuestion(student=request.user, question=q).save()
                    return JsonResponse({'status': "success"})
    return JsonResponse({"status": "failure"})

@student_required
def dislike(request):
    if request.method == "POST":
        if request.is_ajax():
            if "questionID" in request.POST:
                id = request.POST["questionID"]
                q = Question.objects.get(id=id)
                likes_number = q.likes
                likes_number -= 1
                q.likes = likes_number
                q.save()
                LikedQuestion.objects.filter(student=request.user).filter(question=q).delete()
                return JsonResponse({'status': "success"})
    return JsonResponse({"status": "failure"})

@student_required
def student_courses(request):
    student = request.user
    if not student.andrewID:
        email = student.email
        andrew_id = email.split('@')[0]
        student.andrewID = andrew_id
        student.save()
    courses = Course.objects.filter(students=student)
    return render(request, 'qq/student_courses.html', {'courses': courses})

@student_required
def enter_new_queue(request):
    if request.method == 'POST':
        if 'new_queue' in request.POST and 'new_course_num' in request.POST and 'new_invitation_code' in request.POST:
            new_course_num = request.POST.get('new_course_num')
            new_invitation_code = request.POST.get('new_invitation_code')
            # check if the course exists
            if Course.objects.filter(course_number=new_course_num).exists():
                # check if the invitation code is correct
                if Course.objects.filter(course_number=new_course_num, invitation_code=new_invitation_code).exists():
                    course = Course.objects.filter(course_number=new_course_num, invitation_code=new_invitation_code)[0]
                    # check if the student has already joined the same course
                    if StudentCourse.objects.filter(student=request.user, course = course).exists():
                        messages.warning(request, 'You have already joined course ' + new_course_num + '-' + course.course_name + '!')
                    else:
                        StudentCourse(student=request.user, course=course, bonus=0).save()
                        course.students.add(request.user)
                else:
                    messages.warning(request, 'Incorrect invitation code! Please try again.')
            else:
                messages.warning(request, 'Course does not exist! Make sure you have entered the correct course number.')
    return student_courses(request)

@student_required
def get_my_question(request, course_id):
    if request.method == "GET":
        student = request.user
        questions = Question.objects.filter(lecture__course__id=course_id, student=student).order_by('-lecture__id')
        json = []
        for question in questions:
            # get answers
            answers = Answer.objects.filter(question=question)
            answers_str = []
            count = 1
            for ans in answers:
                answers_display = '<li class="list-group-item">Answer'
                answers_display += str(count)
                answers_display += ' : '
                answers_display += ans.content
                answers_display += '</li>'
                count = count + 1
                answers_str.append(answers_display)

            json.append({"id":question.id,'title':question.title,"description":question.description,"likes":question.likes,"answers":answers_str})

        return JsonResponse({'questions': list(json)})

@student_required
def get_liked_question(request, course_id):
    if request.method == "GET":
        student = request.user
        questions = LikedQuestion.objects.filter(student=student, question__lecture__course__id=course_id)
        liked_questions = Question.objects.filter(likedquestion__in=questions).order_by('-lecture__id')
        json = []
        for question in liked_questions:
            # get answers
            answers = Answer.objects.filter(question=question)
            answers_str = []
            count = 1
            for ans in answers:
                answers_display = '<li class="list-group-item">Answer'
                answers_display += str(count)
                answers_display += ' : '
                answers_display += ans.content
                answers_display += '</li>'
                count = count + 1
                answers_str.append(answers_display)

            json.append({"id":question.id,'title':question.title,"description":question.description,"likes":question.likes,"answers":answers_str})

        return JsonResponse({'questions': list(json)})

@student_required
def exit_course(request):
    if request.method == "POST":
        if 'course_id' in request.POST:
            course_id = request.POST.get('course_id')
            course = Course.objects.get(id=course_id)
            student = request.user
            course.students.remove(student)
            StudentCourse.objects.filter(student=request.user).filter(course_id=course_id).delete()
    return student_courses(request)

@student_required
def my_questions(request, course_id):
    course = Course.objects.get(id=course_id)
    context = {'course': course}
    return render(request, 'qq/questions.html', context)


# Instructor End

@instructor_required
def professor_courses(request):
    instructor = request.user
    if not instructor.andrewID:
        email = instructor.email
        andrew_id = email.split('@')[0]
        instructor.andrewID = andrew_id
        instructor.save()
    courses = Course.objects.filter(instructors=instructor)
    return render(request, 'qq/professor_courses.html', {"courses": courses})

@instructor_required
def add_new_course(request):
    if request.method == "POST":
        if "course_number" in request.POST and "course_name" in request.POST and "invitation_code" in request.POST:
            course_number = request.POST["course_number"]
            course_name = request.POST["course_name"]
            invitation_code = request.POST["invitation_code"]
            instructor = request.user
            #check if the course already exists
            if Course.objects.filter(course_number=course_number).exists():
                message = 'Invalid course number! Course ' + course_number + ' already exists!'
                messages.warning(request, message)
            else:
                course = Course(course_name=course_name, course_number=course_number, invitation_code=invitation_code)
                course.save()
                course.instructors.add(instructor)
                # add default lecture
                time = datetime.today().date()
                lecture_title = "default lecture"
                lecture = Lecture(date=time, title=lecture_title, course=course)
                lecture.save()
    return professor_courses(request)

@instructor_required
def join_existing_course(request):
    if request.method == "POST":
        if 'join_existing_course' in request.POST and 'course_num' in request.POST and 'invitation_code' in request.POST:
            course_num = request.POST.get('course_num')
            invitation_code = request.POST.get('invitation_code')
            # check if the course exists
            if Course.objects.filter(course_number=course_num).exists():
                # check if the invitation code is correct
                if Course.objects.filter(course_number=course_num, invitation_code=invitation_code).exists():
                    course = Course.objects.filter(course_number=course_num, invitation_code=invitation_code)[0]
                    # check if the student has already joined the same course
                    if request.user in course.instructors.all():
                        messages.warning(request, 'You have already joined course <' + course_num + '-' + course.course_name + '> as an instructor !')
                    else:
                        course.instructors.add(request.user)
                        course.save()
                else:
                    messages.warning(request, 'Incorrect invitation code! Please try again.')
            else:
                messages.warning(request, 'Course does not exist! Make sure you have entered the course number correctly.')
        return professor_courses(request)

@instructor_required
def delete_course(request):
    if request.method == "POST":
        if "course_id" in request.POST:
            course_id = request.POST["course_id"]
            Course.objects.get(id=course_id).delete()
    return professor_courses(request)

@ta_or_instructor_required
def get_answers(request):
    if request.method == "POST":
        if request.is_ajax():
            lecture_id = request.POST["lecture_id"]
            lecture = Lecture.objects.get(id=lecture_id)
            questions = Question.objects.filter(lecture=lecture).order_by('-likes').values()
            answer_dict = {}
            for q in Question.objects.filter(lecture=lecture).order_by('-likes'):
                answer_dict[q.pk] = serializers.serialize('json', Answer.objects.filter(question=q).all())
        return JsonResponse({'questions': list(questions), 'answers': json.dumps(answer_dict)})

#@instructor_required
@ta_or_instructor_required
def professor_lecture(request):
    if request.method == "POST":
        if "course_id" in request.POST:
            course_id = request.POST["course_id"]
            course = Course.objects.get(id=course_id)
            lectures = Lecture.objects.filter(course_id=course_id)
    return render(request, 'qq/professor_lectures.html', {"course": course, "lectures": lectures})

@ta_required
def ta_join_existing_course(request):
    if request.method == "POST":
        if 'course_num' in request.POST and 'invitation_code' in request.POST:
            course_num = request.POST.get('course_num')
            invitation_code = request.POST.get('invitation_code')
            # check if the course exists
            if Course.objects.filter(course_number=course_num).exists():
                # check if the invitation code is correct
                if Course.objects.filter(course_number=course_num, invitation_code=invitation_code).exists():
                    course = Course.objects.filter(course_number=course_num, invitation_code=invitation_code)[0]
                    # check if the student has already joined the same course
                    if request.user in course.instructors.all():
                        messages.warning(request, 'You have already joined course <' + course_num + '-' + course.course_name + '> as an TA !')
                    else:
                        course.instructors.add(request.user)
                        course.save()
                else:
                    messages.warning(request, 'Incorrect invitation code! Please try again.')
            else:
                messages.warning(request, 'Course does not exist! Make sure you have entered the course number correctly.')
        return ta_courses(request)

@ta_required
def ta_courses(request):
    instructor = request.user
    courses = Course.objects.filter(instructors=instructor)
    return render(request, 'qq/ta_courses.html', {"courses": courses})

@ta_or_instructor_required
def add_new_lecture(request):
    if request.method == "POST":
        if "course_id" in request.POST and "lecture_title" in request.POST:
            id = request.POST['course_id']
            time = datetime.today().date()
            lecture_title = request.POST["lecture_title"]
            course = Course.objects.get(id=id)
            lecture = Lecture(date=time, title=lecture_title, course=course)
            lecture.save()
            lectures = Lecture.objects.filter(course_id=id)
    return render(request, 'qq/professor_lectures.html', {"course": course, "lectures": lectures})

@ta_or_instructor_required
def delete_lecture(request):
    if request.method == "POST":
        if "lecture_id" in request.POST and "course_id" in request.POST:
            lecture_id = request.POST["lecture_id"]
            id = request.POST["course_id"]
            course = Course.objects.get(id=id)
            lectures = Lecture.objects.filter(course_id=id)
            lectures_num = Lecture.objects.filter(course=course).count()
            if lectures_num>1:
                Lecture.objects.get(id=lecture_id).delete()
            else:
                messages.warning(request, 'Should have at least one lecture')
                return render(request, 'qq/professor_lectures.html',
                              {"course": course, "lectures": lectures})
    return render(request, 'qq/professor_lectures.html', {"course": course, "lectures": lectures})

@ta_or_instructor_required
def submitAnswer(request):
    if request.is_ajax():
        text = request.POST["text"]
        question_id = request.POST["question"]
        course_id = request.POST['course']
        if not re.match(r'\s+',text):
            q = Question.objects.get(pk=question_id)
            answer = Answer(question=q)
            answer.save()
            answer.content = text
            answer.save()
            # add bonus to the student
            course = Course.objects.get(pk=course_id)
            student = q.student
            cs = StudentCourse.objects.get(course=course, student=student)
            cs.bonus += int(request.POST["bonus"])
            cs.save()
    return JsonResponse({'question': question_id, 'answer': text})

def answers(request):
    if request.method =="POST":
        course_id  = request.POST["course_id"]
        course = Course.objects.get(id=course_id)
        lecture_id  = request.POST["lecture_id"]
        lecture = Lecture.objects.get(id=lecture_id)

        return render(request, 'qq/answers.html', {"course":course, "lecture":lecture})

@ta_or_instructor_required
def deleteQuestion(request):
    if request.method == "POST":
        if request.is_ajax():
            question_id = request.POST["question_id"]
            Question.objects.get(id=question_id).delete()

        return JsonResponse({'success': "successfully deleted!"})

def enter_leaderboard(request):
    if request.method == "POST":
        if "course_id" in request.POST:
            course_id = request.POST["course_id"]
            course = Course.objects.get(pk=course_id)
            return render(request, 'qq/leaderboard.html', {"course_id": course_id, "course_number":course.course_number})
    return index(request)

def get_leaderboard_stu(request):
    if request.method == "GET":
        if "course_id" in request.GET:
            course_id = request.GET["course_id"]
            student_courses = StudentCourse.objects.filter(course_id=course_id)
            json = []
            for student_course in student_courses:
                student = student_course.student
                # get likes of each student
                lectures = Lecture.objects.filter(course_id=course_id)
                like_sum = 0
                count = 0
                for lecture in lectures:
                    questions = Question.objects.filter(lecture=lecture).filter(student=student)
                    for question in questions:
                        like_sum += question.likes
                        count += 1
                json.append({"id": student.id, "name": student.username, "likes_receives": like_sum,
                             "bonus_score": student_course.bonus, "question_raised": count})
            return JsonResponse({"student": list(json)})
    return JsonResponse({"status": "false"})

def questions(request):
    return render(request, 'qq/questions.html')
