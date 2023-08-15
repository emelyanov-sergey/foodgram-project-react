from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True
    )
    email = models.EmailField(
        verbose_name='Email',
        max_length=254,
        unique=True
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        null=False,
        blank=False
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=254,
        null=False,
        blank=False
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=150
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username}: {self.email}'


class Subscriptions(models.Model):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='subscriptions_user'
    )
    author = models.ForeignKey(
        MyUser,
        on_delete=models.Case,
        verbose_name='Автор',
        related_name='subscribers_author'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [models.UniqueConstraint(
            fields=['user', 'author'],
            name='unique_subscription'
        )]

    def __str__(self):
        return f'{self.user} подписался на {self.author}'
