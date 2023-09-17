from django.core.management import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):

    Category.objects.all().delete()

    def handle(self, *args, **options):
        category_list = [
            {'name': 'Мучное', 'description': '...'},
            {'name': 'Напитки', 'description': '...'},
            {'name': 'Сладкое', 'description': '...'}
        ]

        category_for_create = []
        for category in category_list:
            category_for_create.append(
                Category(**category)
            )

        Category.objects.bulk_create(category_for_create)

        products_list = [
            {'name': 'Булка', 'description': '...', 'category': '1', 'cost': '25', 'data_start': '2023-09-16T04:55:20.875Z', 'data_change': '2023-09-16T04:55:20.875Z'},
            {'name': 'Сосиска в тесте', 'description': '...', 'category': '1', 'cost': '37', 'data_start': '2023-09-16T04:55:20.875Z', 'data_change': '2023-09-16T04:55:20.875Z'},
            {'name': 'Шоколад', 'description': '...', 'category': '3', 'cost': '87', 'data_start': '2023-09-16T04:55:20.875Z', 'data_change': '2023-09-16T04:55:20.875Z'},
            {'name': 'Конфеты Маска', 'description': '...', 'category': '3', 'cost': '38', 'data_start': '2023-09-16T04:55:20.875Z', 'data_change': '2023-09-16T04:55:20.875Z'},
            {'name': 'Вода', 'description': '...', 'category': '2', 'cost': '23', 'data_start': '2023-09-16T04:55:20.875Z', 'data_change': '2023-09-16T04:55:20.875Z'},
            {'name': 'Кока-кола', 'description': '...', 'category': '2', 'cost': '56', 'data_start': '2023-09-16T04:55:20.875Z', 'data_change': '2023-09-16T04:55:20.875Z'}
        ]

        product_for_create = []
        for product in products_list:
            product_for_create.append(
                Product(**product)
            )

        Product.objects.bulk_create(product_for_create)