from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='название категории')
    description = models.TextField(verbose_name='описание категории')

    def __str__(self):
        # Строковое отображение объекта
        return f'{self.pk} {self.name}'

    class Meta:
        verbose_name = 'категория'  # Настройка для наименования одного объекта
        verbose_name_plural = 'категории'  # Настройка для наименования набора объектов


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='наименование товара', unique=True)
    description = models.TextField(verbose_name='описание товара')
    preview = models.ImageField(upload_to='product_images', **NULLABLE, verbose_name='превью')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория')
    cost = models.IntegerField(verbose_name='стоимость')
    created_at = models.DateTimeField(verbose_name='дата создания', **NULLABLE, auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='дата последнего изменения', auto_now=True, **NULLABLE)

    def __str__(self):
        # Строковое отображение объекта
        return f'{self.pk} {self.name} {self.cost} {self.category}'

    class Meta:
        verbose_name = 'продукт'  # Настройка для наименования одного объекта
        verbose_name_plural = 'продукты'  # Настройка для наименования набора объектов


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='товар', **NULLABLE)
    number = models.IntegerField(verbose_name='номер версии', default=1)
    title = models.CharField(max_length=150, verbose_name='название версии')
    feature = models.BooleanField(verbose_name='признак текущей версии', default=True)
