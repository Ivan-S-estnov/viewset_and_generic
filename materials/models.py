from django.conf import settings
from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название курса")
    preview = models.ImageField(
        upload_to="materials/preview/",
        verbose_name="превью курса",
        blank=True,
        null=True,
    )
    description = models.TextField(verbose_name="Описание курса", blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="Укажите владельца курса",
    )
    link = models.URLField(verbose_name="url-курса", blank=True, null=True)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название урока")
    preview = models.ImageField(
        upload_to="materials/preview/",
        verbose_name="превью урока",
        blank=True,
        null=True,
    )
    description = models.TextField(verbose_name="Описание урока", blank=True, null=True)
    course = models.ForeignKey(
        "Course",
        on_delete=models.CASCADE,
        verbose_name="Курс",
        related_name="lessons",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="Укажите владельца урока",
    )
    link = models.URLField(verbose_name="url-урока", blank=True, null=True)

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.name

class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="subscription_user",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        related_name="subscription_course",
    )

    def __str__(self):
        return f"{self.user} - {self.course}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
