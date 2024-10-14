from django.urls import path
from .api import *

urlpatterns = [
    path('', AmenitiesViewSet.as_view({'get': 'list'}), name='amenities-list'),
       
]