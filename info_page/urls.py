from django.urls import path
from .views import external_redirect,preview_block
# from .api import PreviewPagesViewSet, PagesSeoViewSet
urlpatterns = [

   path('preview/<str:locale>/<slug:slug>/', external_redirect, name='external-redirect'),
#    path('page-preview/<slug:slug>/', PreviewPagesViewSet.as_view({'get': 'retrieve'}), name='page-privew'),
#    path('page-seo/<slug:slug>/', PagesSeoViewSet.as_view({'get': 'retrieve'}), name='page-seo'),
]