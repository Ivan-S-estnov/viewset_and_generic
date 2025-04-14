from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название курса")
    preview = models.ImageField(
        upload_to="materials/preview/",
        verbose_name="превью курса",
        blank=True,
        null=True,
    )
    description = models.TextField(
        verbose_name="Описание курса", blank=True, null=True
    )

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
    description = models.TextField(
        verbose_name="Описание урока", blank=True, null=True
    )
    course = models.ForeignKey(
        "Course",
        on_delete=models.SET_NULL,
        verbose_name="Курс",
        blank=True,
        null=True,
        related_name="lessons",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["course", "name"]

    def __str__(self):
        return self.name
