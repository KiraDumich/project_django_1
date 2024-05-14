from django.core.cache import cache
from django.urls import path, reverse_lazy
from django.views.decorators.cache import cache_page

from blog.views import BlogListView
from catalog.apps import CatalogConfig
from catalog.views import (CatalogView, ContactsView, ProductDeleteView, ProductListView, ProductUpdateView,
                           ProductDetailView, ProductCreateView, CategoryListView)

app_name = CatalogConfig.name
urlpatterns = [
    path('', CatalogView.as_view(), name='main'),
    path('catalog/', ProductListView.as_view(), name='home'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('<int:pk>/view/', cache_page(60)(ProductDetailView.as_view()), name='view'),
    path('create/', ProductCreateView.as_view(), name='create'),
    path('edit/<int:pk>/', ProductUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete'),
    path('categories/', CategoryListView.as_view(), name='categories_list')

]

