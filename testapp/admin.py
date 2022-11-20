from django.contrib import admin
from .models import Teacher, Student, Subject, Group, Submition, Course, Test, Quetion, Answer

admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Group)
admin.site.register(Course)
admin.site.register(Test)
admin.site.register(Quetion)
admin.site.register(Answer)
admin.site.register(Submition)