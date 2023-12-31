# Generated by Django 4.2.4 on 2023-09-15 09:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tasksolver", "0006_remove_image_url_image_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProcessParameters",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("saturation", models.IntegerField()),
                ("brightness", models.IntegerField()),
                ("blur", models.IntegerField()),
            ],
        ),
    ]
