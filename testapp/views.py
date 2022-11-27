import json

from math import ceil
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render
from django.views import View

from testapp.funcs import create_random_chars, get_correct, cut_by_page

from .models import (Answer, Course, Group, Quetion, Student, Subject, Teacher,
                     Test, Submition)


@login_required(login_url='login')
def profile_view(request):
    current_teacher = Teacher.objects.all().filter(user_id=request.user)
    if current_teacher:
        subjects = current_teacher[0].subjects.all()
        courses = Course.objects.filter(users__in=[request.user])
        ctx = {'teacher' : current_teacher[0], 'subjects' : subjects, 'courses' : courses}
        return render(request, 'testapp/teacher_profile.html', ctx)
    else:
        current_student = Student.objects.get(user_id=request.user)
        courses = Course.objects.filter(users__in=[request.user])
        ctx = {'student' : current_student, 'courses' : courses}
        return render(request, 'testapp/student_profile.html', ctx)


class ProfileEditView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.status == 'T':
                current_teacher = Teacher.objects.get(user_id=request.user)
                subjects = Subject.objects.all()
                sel_subjects = Subject.objects.filter(teachers__in=[current_teacher])
                ctx = {
                    'teacher' : current_teacher,
                    'subjects' : subjects,
                    'sel_subjects' : sel_subjects,
                }
                return render(request, 'testapp/teacher_edit.html', ctx)
            else:
                current_student = Student.objects.get(user_id=request.user)
                groups = Group.objects.all()
                ctx = {'student' : current_student, 'groups' : groups}
                return render(request, 'testapp/student_edit.html', ctx)
        else:
            return redirect('login')
    def post(self, request):
        if request.user.status == 'T':
            args = request.POST
            name = args.get('full_name')
            contacts = args.get('contacts')
            subjects = args.getlist('subjects')
            teacher = Teacher.objects.get(user_id=request.user)
            teacher.subjects.clear()
            for subject in subjects:
                sub_obj = Subject.objects.get(subject_name=subject)
                teacher.subjects.add(sub_obj)
            teacher.full_name = name
            teacher.contacts = contacts
            teacher.save()
        else:
            args = request.POST
            name = args.get('full_name')
            if args.get('group') == 'add':
                try:
                    group = Group.objects.get(group_code=args.get('n_group'))
                except:
                    group = Group(group_code=args.get('n_group'))
                    group.save()
            else:
                group = Group.objects.get(group_code=args.get('group'))
            student = Student.objects.get(user_id=request.user)
            student.full_name = name
            student.group = group  
            student.save()

        return redirect('profile')


class NewCourseView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.status == 'T':
                return render(request, 'testapp/new_course.html')
            else:
                return HttpResponseNotFound()
        else:
            return redirect('login')

    def post(self, request):
        args = request.POST
        if request.user.status == 'T':
            name = args.get('name')
            desc = args.get('description')
            code = create_random_chars(10)
            new_course = Course(title=name, description=desc, code=code)
            new_course.save()
            new_course.users.add(request.user)
            return redirect('course', code=code)
        else:
            return HttpResponse('Курс не знайдено')


class SubjectAddingView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.status == 'T':
                return render(request, 'testapp/add_subject.html')
            else:
                return HttpResponseNotFound()
        else:
            return redirect('login')

    def post(self, request):
        if request.user.status == 'T':
            new_sub = request.POST.get('subject')
            try:
                created_sub = Subject.objects.get(subject_name=new_sub)
            except:
                created_sub = Subject(subject_name=new_sub)
                created_sub.save()
            if request.POST.get('add'):
                created_sub.teachers.add(Teacher.objects.get(user_id=request.user))
        return redirect('profile')


class JoinCourseView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'testapp/enter_course.html')
        else:
            return redirect('login')

    def post(self, request):
        args = request.POST
        code = args.get('code')
        try:
            course = Course.objects.get(code=code)
            course.users.add(request.user)
            return redirect('course', code=code)
        except:
            return HttpResponse('Курс не знайдено')


class CourseView(View):
    def get(self, request, code):
        if request.user.is_authenticated:
            try:
                course = Course.objects.get(code=code)
                teachers = course.users.all().filter(status='T')
                tusers = []
                for user in teachers:
                    tuser = Teacher.objects.get(user_id=user)
                    tusers.append(tuser)
                tests = Test.objects.filter(course=course)
                ctx = {'course' : course, 'teachers' : tusers, 'tests' : tests}
                if request.user in course.users.all():
                    return render(request, 'testapp/course.html', ctx)
                else:
                    return HttpResponseNotFound()
            except:
                return HttpResponseNotFound()

            # course = Course.objects.get(code=code)
            # teachers = course.users.all().filter(status='T')
            # tusers = []
            # for user in teachers:
            #     tuser = Teacher.objects.get(user_id=user)
            #     tusers.append(tuser)
            # tests = Test.objects.filter(course=course)
            # print(tests)
            # ctx = {'course' : course, 'teachers' : tusers, 'tests' : tests}
            # if request.user in course.users.all():
            #     return render(request, 'testapp/course.html', ctx)
            # else:
            #     return HttpResponseNotFound()
        else:
            return redirect('login')


class NewTestView(View):
    def get(self, request, code):
        return render(request, 'testapp/newtest.html', {"code" : code})

    def post(self, request, code):
        args = request.POST
        print(json.loads(request.POST.get('q')))
        t = Test(title=args.get('qname'), description=args.get('desc'),
            time_to_submit=args.get('time'), time_to_publish=args.get('pub_time'),
            max_points=args.get('m_points'), course=Course.objects.get(code=code))
        t.save()
        for quetion in json.loads(request.POST.get('q')):
            q = Quetion(content=quetion.get('text'),
            points=quetion.get('points'), test=t)
            q.save()
            for answer in quetion.get('ans'):
                a = Answer(content=answer.get('text'),
                is_correct=answer.get('is_correct'), quetion=q)
                a.save()
        return HttpResponse()


class TestView(View):
    def get(self, request, code, id):
        course = Course.objects.get(code=code)
        tests = Test.objects.filter(course=course)
        test = tests.get(id=id)
        quetions = Quetion.objects.filter(test=test)
        out = []
        for quet in quetions:
            corrects = 0
            answers = list(Answer.objects.filter(quetion=quet))
            for answer in answers:
                if answer.is_correct:
                    corrects += 1
            if corrects > 1:
                type = 'check'
            else:
                type = 'radio'
            out.append({'quetion' : quet, 'answers' : answers, 'type' : type})
        ctx = {'test' : test, 'quetions' : out}
        if request.user.is_authenticated and request.user.status == 'S':
            subs = Submition.objects.filter(test=test)
            student = Student.objects.get(user_id=request.user)
            try:
                submition = subs.get(student=student)
            except Submition.DoesNotExist:
                submition = None
            if not submition:
                new_sub = Submition(submited=False,
                    student=Student.objects.get(user_id=request.user),
                    points=0, test=test)
                new_sub.save()
                
        return render(request, 'testapp/test.html', ctx)

    def post(self, request, code, id):
        course = Course.objects.get(code=code)
        tests = Test.objects.filter(course=course)
        test = tests.get(id=id)
        quetions = Quetion.objects.filter(test=test)
        real_max = 0
        points = 0
        all_answers = []
        for quetion in quetions:
            real_max += quetion.points
            answers = list(Answer.objects.filter(quetion=quetion)) # Надо загнать под функцию
            corrects = 0 # Функцию добавить в funcs.py
            for answer in answers: # функция принимает quetion (type == Quetion)
                if answer.is_correct: # возвращает type == 'check' or type == 'radio'
                    corrects += 1 # После этого переработать метод get()
            if corrects > 1:
                type = 'check'
            else:
                type = 'radio'
            if type == 'radio':
                all_answers.append(request.POST.get(str(quetion.id)))
                if str(get_correct(quetion)) == request.POST.get(str(quetion.id)):
                    points += quetion.points
            elif type == 'check':
                answers = Answer.objects.filter(quetion=quetion)
                points_per_answer = quetion.points / len(answers)
                for ans in answers:
                    print(request.POST.get(str(ans.id)))
                    if request.POST.get(str(ans.id)) and ans.is_correct:
                        points += points_per_answer
                        all_answers.append(str(ans.id))
                    elif not request.POST.get(str(ans.id)) and not ans.is_correct:
                        points += points_per_answer
        mark = int(test.max_points*(points/real_max))
        subs= Submition.objects.filter(test=test)
        sub = subs.get(student=Student.objects.get(user_id=request.user))
        sub.points = mark
        sub.submited = True
        for answer in all_answers:
            sub.answers.add(Answer.objects.get(id=int(answer)))
            print(Answer.objects.get(id=int(answer)).content)
        sub.save()
        return redirect('course', code)


@login_required(login_url='login')
def testoverview(request, code, id):
    if request.user.status == 'T':
        test = Test.objects.get(id=id)
        course = Course.objects.get(code=code)
        submitions = Submition.objects.filter(test=test)
        ctx = {'test' : test, 'subs' : submitions}
        return render(request, 'testapp/test_overview.html', ctx)


@login_required(login_url='login')
def courseoverview(request, code):
    if request.user.status != 'T':
        return HttpResponseNotFound()
    course = Course.objects.get(code=code)
    tests = Test.objects.filter(course=course)
    s_users = course.users.filter(status='S')
    students = []
    for s_user in s_users:
        student = Student.objects.get(user_id=s_user)
        students.append(student)
    pages = ceil(len(tests)/5)
    if request.GET.get('page'):
        page = int(request.GET.get('page'))
    else:
        page = 1
    tests = cut_by_page(tests, page)
    out = []
    for student in students:
        subs = Submition.objects.filter(student=student)
        marks = []
        for test in tests:
            try:
                sub = subs.get(test=test)
            except Submition.DoesNotExist:
                sub = None
            if sub:
                mark = sub.points
            else:
                mark = 'N/A'
            marks.append(mark)
        out.append({'student' : student, 'marks' : marks})
    ctx = {'course' : course, 'tests' : tests, 'students' : out, 'pages' : pages, 'page' : page}
    return render(request, 'testapp/course_overview.html', ctx)
