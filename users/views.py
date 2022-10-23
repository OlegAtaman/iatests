from django.shortcuts import render, redirect
from django.views import View
from .forms import UserCreationForm
from django.contrib.auth import authenticate, login

class RegisterView(View):

    template_name = 'registration/registration.html'

    def get(self, request):
        ctx = {
            'form' : UserCreationForm()
        }
        return render(request, self.template_name, ctx)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('main')

        ctx = {
            'form' : form
        }
        return render(request, self.template_name, ctx)