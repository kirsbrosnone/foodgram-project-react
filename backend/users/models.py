from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUser(AbstractUser):
    """Кастомный класс пользователя."""
    email = models.EmailField(
        max_length=254, unique=True, blank=False, null=False,
        help_text='Адрес электронной почты',
    )
    username = models.CharField(
        max_length=150, unique=True, blank=False,
        help_text='Уникальный юзернейм',
    )
    first_name = models.CharField(
        max_length=150, blank=False,
        help_text='Имя',
    )
    last_name = models.CharField(
        max_length=150, blank=False,
        help_text='Фамилия'
    )


class Subscribe(models.Model):
    """Класс подписок пользователя."""
    user = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name='follower'
    )
    following = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, related_name='following'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_follower'
            )
        ]
