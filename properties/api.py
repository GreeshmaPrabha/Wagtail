from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from wagtail.models import Locale
from django.utils.translation import get_language_from_request
from .models import PropertyIndexPage,PropertyPage
from .serializers import *
from django.db.models import Prefetch,Q
from django.db.models import F, Value, IntegerField, FloatField
from django.db.models.functions import Cast
from .blocks import *

# Create your views here.
class PropertyPageViewSet(viewsets.ModelViewSet):
    serializer_class = PropertyPageSerializer
    

    def get_queryset(self):
        #lang = self.request.query_params.get('lang', 'en')
        lang = get_language_from_request(self.request)
        locale = get_object_or_404(Locale, language_code=lang)
        return PropertyPage.objects.live().exact_type(PropertyPage).filter(locale=locale)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        #context['language'] = self.request.query_params.get('lang', 'en')
        context['language'] = get_language_from_request(self.request)
        return context
    
    
    def get_serializer_class(self):
        group_serializer = {
            'list': PropertyPageSerializer,
            # 'retrieve': PropertyPageDetailSerializer,
        }
        
        # Get the appropriate serializer based on the action
        serializer_class = group_serializer.get(self.action, None)
        
        if serializer_class is None:
            raise ValueError(f"No serializer found for action: {self.action}")
        return super().get_serializer_class()
    
    
    def list(self, request, *args, **kwargs):
        response= {}
        lang = request.query_params.get('lang', 'en')
        queryset = self.get_queryset()
        
        sort_by = request.GET.get('sort', 'latest')
        search = request.GET.get('search', None)
        rent_filter = request.GET.get('rent_filter', None)
        type_filter = request.GET.get('type_filter', None)
        bed_filter = request.GET.get('bed_filter', None)
        results = []
        filter_query = Q()
        search_query = Q()
        if sort_by:    
            if sort_by == 'latest':
                queryset = queryset.order_by('-first_published_at')
            elif sort_by == 'oldest':
                queryset = queryset.order_by('first_published_at')

        for page in queryset:
            for block in page.content:
                if block.block_type == 'property_block':
                    # Retrieve the title, location, and property
                    title = block.value.get('title', '')
                    location = block.value.get('location', '')
                    property_name = block.value.get('property', '')
                
                    if search:
                        # Add conditions to the search_query
                        if search.lower() in title.lower():
                            search_query |= Q(id=page.id)
                        elif search.lower() in location.lower():
                            search_query |= Q(id=page.id)
                        elif search.lower() in property_name.lower():
                            search_query |= Q(id=page.id)
                        
            queryset = queryset.filter(search_query)
        
        for page in queryset:
            for block in page.content:
                if block.block_type == 'property_block':
                    amount = block.value.get('amount', '')
                    type_choice = block.value.get('type_choice', '')
                    bedroom_count = block.value.get('bedroom_count', '')                    
                    
                    if rent_filter and rent_filter in amount:
                        filter_query |= Q(id=page.id)
                    if type_filter and type_filter == type_choice:
                        filter_query |= Q(id=page.id)
                    if bed_filter and bed_filter == bedroom_count:
                        filter_query |= Q(id=page.id)
            queryset = queryset.filter(filter_query)
                
        
        serializer = self.get_serializer(queryset, many=True, context={'language': lang, 'request': request})
        response['result'],response['records'] = 'success',serializer.data
        return Response(response, status=status.HTTP_200_OK)
    
    
    def retrieve(self, request, *args, **kwargs):
        response = {}
        try:  
            # Extract slug from URL parameters
            slug = kwargs.get('slug')
            
            # Get language from the request and fetch corresponding Locale object
            lang = get_language_from_request(request)
            locale = get_object_or_404(Locale, language_code=lang)
            
            # Create a queryset for PropertyPage filtered by locale and live pages
            queryset = PropertyPage.objects.live().exact_type(PropertyPage).filter(locale=locale)
            
            # Fetch the specific PropertyPage using slug, raising a 404 if not found
            property_page = get_object_or_404(queryset, slug=slug)
            
            # Serialize the retrieved PropertyPage
            serializer = self.get_serializer(property_page,context={'slug':slug,'locale':locale})
            
            # Prepare the response data
            response['result'] = 'success'
            response['records'] = serializer.data
        except Exception as e:
            response['result'] = 'failure'
            response['message'] = str(e)
        # Return the response with a 200 OK status
        return Response(response, status=status.HTTP_200_OK)