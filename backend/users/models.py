from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Кастомный класс пользователя."""
    username = models.CharField('Никнейм', max_length=150, unique=True)
    first_name = models.CharField('Имя', max_length=150, blank=False)
    last_name = models.CharField('Фамилия', max_length=150, blank=False)
    email = models.EmailField(
        'Электронная почта', max_length=254, unique=True, blank=False,
        null=False
    )


class Follow(models.Model):
    """Класс подписок."""

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='follower',
        help_text='Подписчик',
    )
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='author',
        help_text='Автор',
    )

    class Meta:
        verbose_name = 'Подписка на автора'
        verbose_name_plural = 'Подписка на авторов'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follower'
            )
        ]
