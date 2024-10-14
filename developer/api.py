from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from wagtail.models import Locale
from django.utils.translation import get_language_from_request
from .models import DeveloperPage
from .serializers import *
from django.db.models import Prefetch,Q
from django.db.models import F, Value, IntegerField, FloatField
from django.db.models.functions import Cast
from .blocks import *
from mysite.constantvariables import PAGINATION_PERPAGE
from django.core.paginator import Paginator
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt




# Create your views here.
class DeveloperPageViewSet(viewsets.ModelViewSet):
    # serializer_class = PropertyNewPageSerializer
    

    def get_queryset(self):
        #lang = self.request.query_params.get('lang', 'en')
        lang = get_language_from_request(self.request)
        locale = get_object_or_404(Locale, language_code=lang)
        return DeveloperPage.objects.live().exact_type(DeveloperPage).filter(locale=locale)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        #context['language'] = self.request.query_params.get('lang', 'en')
        context['language'] = get_language_from_request(self.request)
        return context
    
    
    def get_serializer_class(self):
        group_serializer = {
            'list': DeveloperPageSerializer,
            # 'retrieve': PropertyNewDetailPageSerializer,
        }
        
        if self.action in group_serializer.keys():
            return group_serializer[self.action]
        
        
    def list(self, request, *args, **kwargs):
        response= {}
        lang = request.query_params.get('lang', 'en')
        queryset = self.get_queryset()
        limit = int(request.GET.get('limit', PAGINATION_PERPAGE))  # Ensure limit is an integer
        page = int(request.GET.get('page', 1))
        
        # lang = get_language_from_request(self.request)
            
        # # Get the locale object or raise a 404 error if not found
        locale = get_object_or_404(Locale, language_code=lang)
                
        if queryset:
            pagination = Paginator(queryset, limit)
            records = pagination.get_page(page)
            has_next = records.has_next()
            has_previous = records.has_previous()
            
            serializer = self.get_serializer(queryset, many=True, context={'language': lang, 'request': request,"locale":locale})
            response['result'],response['records'],response['page_count'],response['pages'],response['has_next'],response['has_previous'] = 'success',serializer.data, pagination.count,pagination.num_pages,has_next, has_previous
            return Response(response, status=status.HTTP_200_OK)
        return Response({'result': 'failed', 'message': 'No data found'}, status.HTTP_400_BAD_REQUEST)
        