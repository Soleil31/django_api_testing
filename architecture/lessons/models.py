from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.db.models import Sum


class Product(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_product_stats(self):
        total_lessons_watched = LessonStatus.objects.filter(
            lesson__products=self,
            status=LessonStatus.Status.WATCHED
        ).count()

        total_time_watched = LessonStatus.objects.filter(
            lesson__products=self,
            status=LessonStatus.Status.WATCHED
        ).aggregate(Sum('watched_time'))['watched_time__sum']

        total_students = Access.objects.filter(product=self).count()

        purchase_percentage = (Access.objects.filter(product=self).count() * 100) / User.objects.count()

        return {
            'total_lessons_watched': total_lessons_watched,
            'total_time_watched': total_time_watched,
            'total_students': total_students,
            'purchase_percentage': purchase_percentage,
        }

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
    
    def get_lesson_status(self):
        try:
            product = self.products.first()  # Получаем первый связанный продукт
            access = Access.objects.get(user=product.owner, product=product)
            return LessonStatus.objects.filter(user=access.user, lesson=self).latest('id')
        except (Access.DoesNotExist, LessonStatus.DoesNotExist):
            return None



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
    watched_at = models.DateTimeField(default=None, null=True, blank=True)


@receiver(post_save, sender=LessonStatus)
def update_lesson_status(sender, instance, **kwargs):
    if instance.watched_time >= 0.8 * instance.lesson.duration:
        instance.status = LessonStatus.Status.WATCHED
        instance.save()
    if instance.status == LessonStatus.Status.WATCHED:
        instance.watched_at = timezone.now()
        instance.save()