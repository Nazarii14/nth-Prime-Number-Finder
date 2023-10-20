# Generated by Django 4.2.4 on 2023-09-15 09:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tasksolver", "0007_processparameters"),
    ]

    operations = [
        migrations.AlterField(
            model_name="processparameters",
            name="blur",
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name="processparameters",
            name="brightness",
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name="processparameters",
            name="saturation",
            field=models.FloatField(default=0.0),
        ),
    ]