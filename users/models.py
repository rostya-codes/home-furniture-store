from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    image = models.ImageField(upload_to='users/images', blank=True, null=True, verbose_name='Аватар')

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователя'  # Альтернативное название для отображения в админ панели
        verbose_name_plural = 'Пользователи'  # Множественное число
