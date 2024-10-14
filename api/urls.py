from django.urls import path
from .api import InformationPagesViewSet

urlpatterns = [
    path('', InformationPagesViewSet.as_view({'get': 'list'}), name='infromation-page-list'),
    path('<slug:slug>/', InformationPagesViewSet.as_view({'get': 'retrieve'}), name='infromation-page-detail'),
]

