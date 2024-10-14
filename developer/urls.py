from django.urls import path
from .api import DeveloperPageViewSet

urlpatterns = [
    path('', DeveloperPageViewSet.as_view({'get': 'list'}), name='developer-list'),
    
]