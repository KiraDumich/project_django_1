from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):

    title = models.CharField(max_length=150, verbose_name='заголовок')
    slug = models.CharField(max_length=100, **NULLABLE, verbose_name='slug')
    text = models.TextField(verbose_name='содержимое')
    preview = models.ImageField(upload_to='preview_image', **NULLABLE, verbose_name='превью')
    start_date = models.DateTimeField(**NULLABLE, verbose_name='дата создания', auto_now_add=True)
    views = models.IntegerField(verbose_name='количество просмотров', default=0)
    public = models.BooleanField(default=True)

    def __str__(self):
        # Строковое отображение объекта
        return {self.title}

    class Meta:
        verbose_name = 'публикация'  # Настройка для наименования одного объекта
        verbose_name_plural = 'публикации'  # Настройка для наименования набора объектов

