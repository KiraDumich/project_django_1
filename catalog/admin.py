from django.contrib import admin
from catalog.models import Category, Product

# admin.site.register(Category)
# admin.site.register(Product)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'cost', 'category')
    list_filter = ('category', 'name')
    search_fields = ('name', 'description')


