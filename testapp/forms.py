from django.forms import ModelForm

from testapp.models import Teacher, Student


class TeacherModelForm(ModelForm):
    class Meta:
        model = Teacher
        fields = ['full_name', 'contacts']


class StudentModelForm(ModelForm):
    class Meta:
        model = Student
        fields = ['full_name', 'group']
