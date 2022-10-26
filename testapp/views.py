from re import template
from tokenize import group
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic.edit import UpdateView
from .models import Teacher, Student, Group
from .forms import TeacherEditForm, StudentEditForm


@login_required(login_url='login')
def profile_view(request):
    current_teacher = Teacher.objects.all().filter(user_id=request.user)
    if current_teacher:
        ctx = {'teacher' : current_teacher[0]}
        print(ctx['teacher'].full_name)
        return render(request, 'testapp/teacher_profile.html', ctx)
    else:
        current_student = Student.objects.get(user_id=request.user)
        ctx = {'student' : current_student}
        return render(request, 'testapp/student_profile.html', ctx)


class ProfileEditView(View, LoginRequiredMixin):
    def get(self, request):
        if request.user.status == 'T':
            # current_teacher = Teacher.objects.get(user_id=request.user)
            # ctx = {'teacher' : current_teacher}
            return render(request, 'testapp/teacher_edit.html', ctx)
        else:
            current_student = Student.objects.get(user_id=request.user)
            groups = Group.objects.all()
            ctx = {'student' : current_student, 'groups' : groups}
            return render(request, 'testapp/student_edit.html', ctx)

    def post(self, request):
        if request.user.status == 'T':
            form = TeacherEditForm(request.POST)
        else:
            args = request.POST
            name = args.get('full_name')
            if args.get('group') == 'add':
                try:
                    group = Group.objects.get(group_code=args.get('n_group'))
                except:
                    group = Group(group_code=args.get('n_group'))
                    group.save()
            student = Student.objects.get(user_id=request.user)
            student.full_name = name
            student.group = group  
            student.save()

        return redirect('profile')
        
            