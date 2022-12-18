from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.views import View

from testapp.models import Group, Student, Teacher

from .forms import UserCreationForm


class RegisterView(View):
    template_name = "registration/registration.html"

    def get(self, request):
        ctx = {"form": UserCreationForm()}
        return render(request, self.template_name, ctx)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            is_teacher = form.cleaned_data.get("is_teacher")
            user = authenticate(username=username, password=password)
            login(request, user)
            if is_teacher:
                teacher = Teacher(
                    user=user
                )
                teacher.save()
                return redirect(f"/teacher/{teacher.pk}/edit")
            else:
                student = Student(
                    user=user
                )
                student.save()
                return redirect(f"/student/{student.pk}/edit")


        ctx = {"form": form}
        return render(request, self.template_name, ctx)
