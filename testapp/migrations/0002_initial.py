# Generated by Django 4.1.4 on 2022-12-17 05:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("testapp", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="teacher",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="submission",
            name="answers",
            field=models.ManyToManyField(to="testapp.answer"),
        ),
        migrations.AddField(
            model_name="submission",
            name="student",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="testapp.student"
            ),
        ),
        migrations.AddField(
            model_name="submission",
            name="test",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="testapp.test"
            ),
        ),
        migrations.AddField(
            model_name="student",
            name="group",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="testapp.group"
            ),
        ),
        migrations.AddField(
            model_name="student",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="question",
            name="test",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="testapp.test"
            ),
        ),
        migrations.AddField(
            model_name="course",
            name="subject",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="testapp.subject"
            ),
        ),
        migrations.AddField(
            model_name="course",
            name="users",
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name="answer",
            name="question",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="testapp.question"
            ),
        ),
    ]
