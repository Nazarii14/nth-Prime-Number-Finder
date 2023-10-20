from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Task(models.Model):
    number = models.IntegerField(default=100,
                                 validators=[MinValueValidator(1), MaxValueValidator(10000000)])
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='tasks_created')
    is_running = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)
    completion_percentage = models.IntegerField(default=0)
    result = models.IntegerField(default=-1)

    class Meta:
        indexes = [
            models.Index(fields=['-number']),
        ]
        ordering = ['-number']

    def __str__(self):
        return str(self.number)
