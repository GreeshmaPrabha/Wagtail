from django.urls import path
from .api import PropertyPageViewSet

urlpatterns = [
    path('', PropertyPageViewSet.as_view({'get': 'list'}), name='property-list'),
    # path('<slug:slug>/', PropertyPageViewSet.as_view({'get': 'retrieve'}), name='property-detail'),
    
]