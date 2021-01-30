from django.db import models

class Lesson(models.Model):
    lesson_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=('Название урока'),
    )

    file = models.FileField(
        verbose_name=('Раздатка'),
    )
    video = models.URLField(
        blank=True,
        null=True,
        verbose_name=('Ссылка на видео')
    )

    class Meta:
        verbose_name = ('Урок')
        verbose_name_plural = ('Уроки')


class User(models.Model):
    login = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=('Логин'),
    )
    password = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=('Пароль'),
    )