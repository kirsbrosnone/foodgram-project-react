from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
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

    anon = 'anon'
    user = 'user'
    moderator = 'moderator'
    admin = 'admin'

    ROLE_CHOICES = [
        (anon, 'Anonymous User'),
        (user, 'Authenticated User'),
        (moderator, 'Moderator'),
        (admin, 'Administrator'),
    ]

    role = models.CharField(choices=ROLE_CHOICES, default=user, max_length=9)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.is_staff is True:
            self.role = self.admin
        super().save(*args, **kwargs)


class Follow(models.Model):
    """Класс подписок пользователя."""

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='follower',
        help_text='Подписчик'
    )
    following = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='following',
        help_text='Автор'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_follower'
            )
        ]
