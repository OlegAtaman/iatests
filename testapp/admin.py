from django.contrib import admin
from .models import Teacher, Student, Subject, Group

admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Group)