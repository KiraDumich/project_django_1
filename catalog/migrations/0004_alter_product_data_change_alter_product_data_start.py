# Generated by Django 4.2.5 on 2023-10-21 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_remove_category_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='data_change',
            field=models.DateTimeField(blank=True, null=True, verbose_name='дата последнего изменения'),
        ),
        migrations.AlterField(
            model_name='product',
            name='data_start',
            field=models.DateTimeField(blank=True, null=True, verbose_name='дата создания'),
        ),
    ]
