# Generated by Django 4.2.4 on 2023-09-14 18:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tasksolver", "0002_remove_task_max_number"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="completed",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="task",
            name="completed_date",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="task",
            name="stage",
            field=models.FloatField(null=True),
        ),
    ]