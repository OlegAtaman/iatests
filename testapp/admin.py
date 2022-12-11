from django.contrib import admin
from .models import Teacher, Student, Subject, Group, Submission, Course, Test, Question, Answer

class TestAdmin(admin.ModelAdmin):
    readonly_fields = ('time_to_publish',)

admin.site.register(Test, TestAdmin)

admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Group)
admin.site.register(Course)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Submission)