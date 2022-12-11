from django.conf import settings
from django.db import models


class Group(models.Model):
    group_code = models.CharField(max_length=5)


class Teacher(models.Model):
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    contacts = models.CharField(max_length=100)
    subjects = models.ManyToManyField('Subject', through='TeachersToSubjects')


class Student(models.Model):
    user_id = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)


class Subject(models.Model):
    subject_name = models.CharField(max_length=50)
    teachers = models.ManyToManyField('Teacher', through='TeachersToSubjects')


class TeachersToSubjects(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)


class Course(models.Model):
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    code = models.CharField(max_length=10)
    title = models.CharField(max_length=50)
    description = models.TextField()


class Test(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    max_points = models.DecimalField(max_digits=10, decimal_places=0)
    time_to_submit = models.TimeField()
    time_to_publish = models.DateTimeField(null=True)
    deadline = models.DateTimeField(null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class Question(models.Model):
    content = models.CharField(max_length=150)
    points = models.DecimalField(max_digits=10, decimal_places=2)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)


class Answer(models.Model):
    content = models.CharField(max_length=150)
    is_correct = models.BooleanField()
    quetion = models.ForeignKey(Question, on_delete=models.CASCADE)


class Submission(models.Model):
    submitted = models.BooleanField(default=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    points = models.DecimalField(max_digits=10, decimal_places=0)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    answers = models.ManyToManyField(Answer)
