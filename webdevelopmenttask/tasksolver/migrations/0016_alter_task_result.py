# Generated by Django 4.2.4 on 2023-09-16 07:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tasksolver", "0015_task_completion_percentage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="result",
            field=models.IntegerField(default=-1),
        ),
    ]