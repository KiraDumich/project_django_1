from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):

    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    country = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    verified = models.BooleanField(default=False, verbose_name='верифицирован', blank=True)
    verified_password = models.CharField(verbose_name='ключ для верификации', **NULLABLE, max_length=20)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return (
            f"{self.email}")

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"
        permissions = [
            (
                'set_user_deactivate',
                'Can deactivate user'
            ),
            ('view_all_users',
             'просмотр всех пользователей'
             ),
        ]
