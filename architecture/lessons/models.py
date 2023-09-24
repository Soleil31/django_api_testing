from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class Product(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

class Access(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

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
    watched_time = models.IntegerField(default=0)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.NOTWATCHED
    )


@receiver(post_save, sender=LessonStatus)
def update_lesson_status(sender, instance, **kwargs):
    if instance.watched_time >= 0.8 * instance.lesson.duration:
        instance.status = LessonStatus.Status.WATCHED
        instance.save()