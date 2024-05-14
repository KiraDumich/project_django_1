# Generated by Django 4.2 on 2024-05-13 11:21

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mail', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='автор'),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='start_datetime_mailing',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 13, 21, 21, 21, 21297), verbose_name='дата и время начала отправки рассылки'),
        ),
    ]
