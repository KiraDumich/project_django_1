from django.urls import path

from blog.views import BlogListView
from catalog.apps import CatalogConfig
from catalog.views import home, contacts, ProductDeleteView, ProductListView, ProductUpdateView, ProductDetailView, ProductCreateView

app_name = CatalogConfig.name
urlpatterns = [
    path('', home, name='main'),
    path('/catalog', ProductListView.as_view(), name='home'),
    path('contacts/', contacts, name='contacts'),
    path('<int:pk>/view/', ProductDetailView.as_view(), name='view'),
    path('create/', ProductCreateView.as_view(), name='create'),
    path('edit/<int:pk>/', ProductUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='delete'),
]
