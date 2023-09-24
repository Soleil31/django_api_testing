from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    access_id = models.IntegerField(max_length=100) #for users to access product


class Lesson(models.Model):
    title = models.CharField(max_length=100)
    video_link = models.URLField()
    duration = models.IntegerField()
    products = models.ManyToManyField(Product)
    created = models.DateTimeField(auto_now_add=True) 
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['-created'])]

    def __str__(self) -> str:
        return self.title or 'Название отсутствует'


class LessonStatus(models.Model):

    class Status(models.TextChoices):
        NOTWATCHED = 'NW', 'Not_watched'
        WATCHED = 'WD', 'Watched'


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    watched_time = models.IntegerField()
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.NOTWATCHED
    )

    def save(self, *args, **kwargs):
        if self.watched_time >= 0.8 * self.lesson.duration:
            self.status = self.Status.WATCHED
        super().save(*args, **kwargs)
