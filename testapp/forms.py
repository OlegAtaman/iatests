from django import forms

from testapp.models import Teacher
from .models import Teacher, Student


class TeacherEditForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('full_name', 'contacts', 'subjects')


class StudentEditForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('full_name', 'group')