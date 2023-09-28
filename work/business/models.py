from django.db import models
from django.conf import settings


class UserLessonStatusChoices(models.TextChoices):

    Viewed = "Viewed", "Просмотрено"
    Not_viewed = "Not viewed", "Не просмотрено"
# Create your models here.


class UserForProduct(models.Model):
    login = models.TextField()

    def __str__(self):
        return f'логин:{self.login}'


class Product(models.Model):
    owner = models.ManyToManyField(
        UserForProduct,
        through='UserProduct',
    )
    product = models.CharField(max_length=50)

    def __str__(self):
        return self.product


class UserProduct(models.Model):
    user = models.ForeignKey(UserForProduct, on_delete=models.CASCADE, related_name='productspos')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='userown')


class Lesson(models.Model):
    title = models.CharField(max_length=50)
    video_url = models.URLField()
    duration = models.IntegerField()
    viewed = models.ManyToManyField(UserForProduct, through='UserLesson')
    product = models.ManyToManyField(Product, through='ProductLesson')


class ProductLesson(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='lessons')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='prods')


class UserLesson(models.Model):
    user = models.ForeignKey(UserForProduct, on_delete=models.CASCADE, related_name='views')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='users')
    viewed_time = models.IntegerField()
    status = models.TextField(
        choices= UserLessonStatusChoices.choices,
        default= UserLessonStatusChoices.Not_viewed
    )

