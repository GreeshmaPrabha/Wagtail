from django.urls import path
from .api import PropertyNewPageViewSet,CurrencyChangeAPIView,FavouritePropertyAPIView

urlpatterns = [
    path('', PropertyNewPageViewSet.as_view({'get': 'list'}), name='property-new-list'),
    path('<slug:slug>/', PropertyNewPageViewSet.as_view({'get': 'retrieve'}), name='property-new-detail'),
    path('<slug:slug>/add-to-fav/', FavouritePropertyAPIView.as_view({'get': 'addtofav'}), name='add-to-fav'),
    path('<slug:slug>/currency-change/', CurrencyChangeAPIView.as_view({'get': 'currencychange'}), name='currency-change'),
    
]


