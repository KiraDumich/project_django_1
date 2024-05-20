# Generated by Django 4.2 on 2024-05-20 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='заголовок')),
                ('slug', models.CharField(blank=True, max_length=100, null=True, verbose_name='slug')),
                ('text', models.TextField(verbose_name='содержимое')),
                ('preview', models.ImageField(blank=True, null=True, upload_to='preview_image', verbose_name='превью')),
                ('start_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='дата создания')),
                ('views', models.IntegerField(default=0, verbose_name='количество просмотров')),
                ('public', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'публикация',
                'verbose_name_plural': 'публикации',
            },
        ),
    ]
