# Generated by Django 4.1.3 on 2022-12-06 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0005_test_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='time_to_publish',
            field=models.DateTimeField(null=True),
        ),
    ]
