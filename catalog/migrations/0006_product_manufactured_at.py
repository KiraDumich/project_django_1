# Generated by Django 4.2.5 on 2024-03-03 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_rename_data_start_product_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='manufactured_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='дата производства'),
        ),
    ]