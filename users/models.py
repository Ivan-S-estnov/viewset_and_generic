from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="Аватар",
        blank=True,
        null=True,
        help_text="Загрузите свой аватар",
    )
    phone = models.CharField(max_length=15, blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    """Класс оплат за курсы или уроки"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    payment_date = models.DateField(verbose_name='Дата оплаты')
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Оплатаченный курс')
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Оплаченный урок')
    amount = models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Сумма оплаты')
    method = models.CharField(max_length=255, verbose_name='Тип оплаты')