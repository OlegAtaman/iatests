from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic.edit import UpdateView
from .models import Subject, Teacher, Student, Group
from .forms import TeacherEditForm, StudentEditForm
from django.http import HttpResponseNotFound


@login_required(login_url='login')
def profile_view(request):
    current_teacher = Teacher.objects.all().filter(user_id=request.user)
    if current_teacher:
        subjects = current_teacher[0].subjects.all()
        ctx = {'teacher' : current_teacher[0], 'subjects' : subjects}
        return render(request, 'testapp/teacher_profile.html', ctx)
    else:
        current_student = Student.objects.get(user_id=request.user)
        ctx = {'student' : current_student}
        return render(request, 'testapp/student_profile.html', ctx)


class ProfileEditView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.status == 'T':
                current_teacher = Teacher.objects.get(user_id=request.user)
                subjects = Subject.objects.all()
                sel_subjects = Subject.objects.filter(teachers__in=[current_teacher])
                ctx = {'teacher' : current_teacher, 'subjects' : subjects, 'sel_subjects' : sel_subjects}
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
