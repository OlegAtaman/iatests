from django.db import models
from django.conf import settings

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
    description = models.CharField(max_length=200)