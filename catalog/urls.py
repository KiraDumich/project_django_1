from django.urls import path
from catalog.views import catalog, contacts

urlpatterns = [
    path('', catalog),
    path('contacts', contacts)
]