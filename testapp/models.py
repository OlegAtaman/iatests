from django.conf import settings
from django.db import models


class Group(models.Model):
    """
    Study group.
    """

    code = models.CharField(max_length=5)

    def __str__(self):
        return self.code


class Subject(models.Model):
    """
    Study subject.
    """

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Course(models.Model):
    """
    A course that students can participate in. In the test app it's mainly used to categorize tests.
    """

    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Teacher(models.Model):
    """
    A professor teaching a class.
    """

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contacts = models.CharField(max_length=100, blank=True)


class Student(models.Model):
    """
    A student taking a class.
    """

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)


class Test(models.Model):
    """
    A test, the cornerstone of the test app.
    A test is related to a course and has publish date, duration, and a deadline.
    """

    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    duration = models.IntegerField(null=True, blank=True)
    published = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Question(models.Model):
    """
    A question, the part and parcel of any test. A test can contain multiple questions.
    The final test grade is calculated as a sum of its questions.
    """

    content = models.CharField(max_length=150)
    points = models.DecimalField(max_digits=10, decimal_places=2)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Answer(models.Model):
    """
    An answer to a question. The question can contain multiple correct answers. Students then choose one or more
    of presented answers and make a submission.
    """

    content = models.CharField(max_length=150)
    is_correct = models.BooleanField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Submission(models.Model):
    """
    Student's submission to a test. Contains answers to questions from the test.
    """

    is_submitted = models.BooleanField(default=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    answers = models.ManyToManyField(Answer)

    def __str__(self):
        return f"Submission to {self.test} by {self.student}"
