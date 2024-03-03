from random import random

from django.core.management import BaseCommand

import json
from catalog.models import Category, Product
from django.db import connection


class Command(BaseCommand):

    def handle(self, *args, **options):
        category_list = []
        for i in range(5):
            category_list.append(
                Category(
                    name=f"Category#{i+1}",
                    description=f"..."
                )
            )

        Category.objects.bulk_create(category_list)

        category_id_list = list(Category.objects.all().values_list('id', flat=True))
        max_id = max(category_id_list)
        min_id = min(category_id_list)

        product_list = []
        for i in range(50):
            product_list.append(
                Product(
                    name=f"Product#{i}",
                    description=f"this is description for product #{i}",
                    category=random.randint(max_id, min_id),
                    cost=random.random() * 1000
                )
            )

        Product.objects.bulk_create(product_list)
    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute(f'TRUNCATE TABLE catalog_category RESTART IDENTITY CASCADE;')

        Category.objects.all().delete()
        Product.objects.all().delete()

        with open('data.json', encoding='utf-8') as json_file:
            data = json.load(json_file)

            product_for_create = []
            category_for_create = []

            for category in data:
                if category["model"] == "catalog.category":
                    category_for_create.append(Category(name=category["fields"]['name'],
                                                        description=category["fields"]['description']))
            Category.objects.bulk_create(category_for_create)
            for product in data:
                if product["model"] == "catalog.product":
                    product_for_create.append(Product(name=product["fields"]['name'],
                                                      description=product["fields"]['description'],
                                                      category=Category.objects.get(pk=product["fields"]['category']),
                                                      cost=product["fields"]['cost']))

            Product.objects.bulk_create(product_for_create)