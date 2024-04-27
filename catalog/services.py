from django.core.cache import cache

from catalog.models import Product, Category
from config import settings


# def cashed_product(product_pk):  # перенесли логику из вьюшек, чтобы увеличить оптимизацию, сервисная прослойка
#     if settings.CASH_ENABLED:
#         key = f'product_{product_pk}'  # Создаем ключ для хранения
#         product_list = cache.get(key)  # Пытаемся получить данные
#         if product_list is None:
#             # Если данные не были получены из кеша, то выбираем из БД и записываем в кеш
#             product_list = Product.objects.filter(product__pk=product_pk)
#             cache.set(key, product_list)
#     else:
#         # Если кеш не был подключен, то просто обращаемся к БД
#         product_list = Product.objects.filter(product__pk=product_pk)
#
#     return product_list


def get_cashed_categories():
        if settings.CASH_ENABLED:
            key = 'category_list'
            category_list = cache.get(key)
            if category_list is None:
                category_list = Category.objects.all()
                cache.set(key, category_list)
        else:
            category_list = Category.objects.all()
        return category_list
