from django.contrib import admin

from .models import (Answer, Course, Group, Question, Student, Subject,
                     Submission, Teacher, Test)


class TestAdmin(admin.ModelAdmin):
    readonly_fields = ("duration",)


admin.site.register(Test, TestAdmin)

admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Group)
admin.site.register(Course)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Submission)
