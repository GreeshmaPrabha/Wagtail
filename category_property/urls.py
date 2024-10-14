from django.urls import path
from .views import get_categories, get_subcategories

urlpatterns = [
    path('api/get-categories/', get_categories, name='get_categories'),
    path('api/get-subcategories/', get_subcategories, name='get_subcategories'),
]