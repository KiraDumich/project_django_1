import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

from config import settings
from config.settings import AUTH_USER_MODEL

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="имя")
    last_name = models.CharField(max_length=100, verbose_name="фамилия")
    surname = models.CharField(max_length=100, verbose_name="отчество", **NULLABLE)
    contact_email = models.EmailField(verbose_name="почта", unique=True)
    comment = models.TextField(
        max_length=300,
        verbose_name="комментарий",
        help_text="Напишите уточняющую информацию",
        **NULLABLE, )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="автор",
        **NULLABLE, )

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.contact_email})"

    class Meta:
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"
        ordering = ("last_name", "first_name", "contact_email")


class Message(models.Model):
    title = models.CharField(
        max_length=100, verbose_name="Тема письма", default="Без темы")
    body = models.TextField(verbose_name="Основное содержание", **NULLABLE)
    owner = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name="автор", **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"
        ordering = ("title",)


class Mailing(models.Model):
    STATUS = [
        ("created", "Создана"),
        ("started", "Запущена"),
        ("finished", "Завершена"),
    ]

    PERIOD_CHOICES = [
        ("every_day", "Ежедневно"),
        ("every_week", "Еженедельно"),
        ("every_month", "Ежемесячно"),
    ]
    start_datetime_mailing = models.DateTimeField(
        verbose_name="дата и время начала отправки рассылки",
        default=datetime.datetime.now(),
    )
    stop_datetime_mailing = models.DateTimeField(
        verbose_name="дата и время окончания отправки рассылки",
        default=datetime.datetime.now,
    )
    mailing_period = models.CharField(
        max_length=25,
        verbose_name="периодичность рассылки",
        choices=PERIOD_CHOICES,
        default="once",
    )
    mailing_status = models.CharField(
        max_length=25,
        verbose_name="статус выполнения рассылки",
        choices=STATUS,
        default="created",
    )

    clients = models.ManyToManyField(Client, verbose_name="клиенты рассылки", related_name='client')
    message = models.ForeignKey(
        Message, verbose_name="сообщение рассылки", on_delete=models.CASCADE, **NULLABLE)
    name = models.CharField(
        max_length=100, verbose_name="название рассылки", **NULLABLE)
    is_active = models.BooleanField(verbose_name="активность рассылки", default=True)
    created_date = models.DateField(
        auto_now_add=True, verbose_name="дата создания", **NULLABLE)
    owner = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name="автор", **NULLABLE)

    def __str__(self):
        return (
            f"{self.name}, Начало {self.start_datetime_mailing}, повтор {self.mailing_period}, "
            f"статус {self.mailing_status}")

    class Meta:
        verbose_name = "рассылка"
        verbose_name_plural = "рассылки"
        permissions = [
            (
                'set_deactivate',
                'Can deactivate mailing'
            ),
            (
                'view_all_mailings',
                'Can view all mailing'
            ),
        ]


class Mail_Log(models.Model):
    STATUS = [("Success", "Успешно"),
              ("No_success", "Неуспешно"),
              ]
    attempt_time = models.DateTimeField(verbose_name='Дата и время последней попытки', **NULLABLE)
    attempt_status = models.CharField(max_length=15, verbose_name='Статус попытки', choices=STATUS,
                                      default="Success")
    server_response = models.TextField(
        verbose_name="ответ почтового сервера", **NULLABLE)

    mailing = models.ForeignKey(
        Mailing, verbose_name="рассылка", on_delete=models.CASCADE, **NULLABLE)
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, verbose_name="клиент рассылки", **NULLABLE)

    def __str__(self):
        return f"Попытка отправки рассылки {self.attempt_time}, статус - {self.attempt_status}"

    class Meta:
        verbose_name = "попытка отправки рассылки"
        verbose_name_plural = "попытки отправки рассылки"
