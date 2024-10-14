from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from wagtail.models import Locale
from django.utils.translation import get_language_from_request
from .models import PropertyNewIndexPage,PropertyNewPage
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
class PropertyNewPageViewSet(viewsets.ModelViewSet):
    # serializer_class = PropertyNewPageSerializer
    

    def get_queryset(self):
        #lang = self.request.query_params.get('lang', 'en')
        lang = get_language_from_request(self.request)
        locale = get_object_or_404(Locale, language_code=lang)
        return PropertyNewPage.objects.live().exact_type(PropertyNewPage).filter(locale=locale)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        #context['language'] = self.request.query_params.get('lang', 'en')
        context['language'] = get_language_from_request(self.request)
        return context
    
    
    def get_serializer_class(self):
        group_serializer = {
            'list': PropertyNewPageSerializer,
            'retrieve': PropertyNewDetailPageSerializer,
        }
        
        if self.action in group_serializer.keys():
            return group_serializer[self.action]
        
        # # Get the appropriate serializer based on the action
        # serializer_class = group_serializer.get(self.action, None)
        
        # if serializer_class is None:
        #     raise ValueError(f"No serializer found for action: {self.action}")
        # return super().get_serializer_class()
        
    def list(self, request, *args, **kwargs):
        response= {}
        lang = request.query_params.get('lang', 'en')
        queryset = self.get_queryset()
        limit = int(request.GET.get('limit', PAGINATION_PERPAGE))  # Ensure limit is an integer
        page = int(request.GET.get('page', 1))
        
        # lang = get_language_from_request(self.request)
            
        # # Get the locale object or raise a 404 error if not found
        locale = get_object_or_404(Locale, language_code=lang)
        
        sort_by = request.GET.get('sort', 'latest')
        search = request.GET.get('search', None)
        rent_filter = request.GET.get('rent_filter', None)
        type_filter = request.GET.get('type_filter', None)
        bed_filter = request.GET.get('bed_filter', None)
        property_type = request.GET.get('property_type', None)
        filter_query = Q()
        # search_query = Q()
                
        if search:
            search_query = Q(location__icontains=search) | Q(property_title__icontains=search)
            queryset = queryset.filter(search_query)
                
        if type_filter:
            filter_query &= Q(type_choice=type_filter) 
        
        if bed_filter:
            filter_query &= Q(bedroom_count=bed_filter) 
            
        if property_type:
            filter_query &= Q(property_type=property_type)
          
        if rent_filter:
            try:
                min_rent, max_rent = map(float, rent_filter.split('-'))
                filter_query &= Q(amount__gte=min_rent, amount__lte=max_rent)
                # filter_query &= Q(amount__gte=min_rent)|Q(amount__lte=max_rent) 
            except ValueError:
                pass 
            
        queryset = queryset.filter(filter_query)
        
        
        
        if sort_by:    
            if sort_by == 'latest':
                queryset = queryset.order_by('-first_published_at')
            elif sort_by == 'oldest':
                queryset = queryset.order_by('first_published_at')
            elif sort_by == 'price low to high':
                queryset = queryset.order_by('amount')
            elif sort_by == 'price high to low':
                queryset = queryset.order_by('-amount')
            elif sort_by == 'sqft low to high':
                queryset = queryset.order_by('-plot')
            elif sort_by == 'sqft high to low':
                queryset = queryset.order_by('plot')
        
        if queryset:
            pagination = Paginator(queryset, limit)
            records = pagination.get_page(page)
            has_next = records.has_next()
            has_previous = records.has_previous()
            
            serializer = self.get_serializer(queryset, many=True, context={'language': lang, 'request': request,"locale":locale})
            response['result'],response['records'],response['page_count'],response['pages'],response['has_next'],response['has_previous'] = 'success',serializer.data, pagination.count,pagination.num_pages,has_next, has_previous
            return Response(response, status=status.HTTP_200_OK)
        return Response({'result': 'failed', 'message': 'No data found'}, status.HTTP_400_BAD_REQUEST)
        
    
    def retrieve(self, request, *args, **kwargs):
        response = {}
        try:
            # Extract slug from URL parameters
            slug = kwargs.get('slug')
            
            # Get language from the request and fetch corresponding Locale object
            lang = get_language_from_request(request)
            locale = get_object_or_404(Locale, language_code=lang)
            
            # Create a queryset for PropertyPage filtered by locale and live pages
            queryset = PropertyNewPage.objects.live().exact_type(PropertyNewPage).filter(locale=locale)
            
            # Fetch the specific PropertyPage using slug, raising a 404 if not found
            property_page = get_object_or_404(queryset, slug=slug)
            
            # Serialize the retrieved PropertyPage
            serializer = self.get_serializer(property_page,context={'slug':slug,'locale':locale,'request': request})
            
            # Prepare the response data
            response['result'] = 'success'
            response['records'] = serializer.data
        except Exception as e:
            response['result'] = 'failure'
            response['message'] = str(e)
        # Return the response with a 200 OK status
        return Response(response, status=status.HTTP_200_OK)
    
    
 
class FavouritePropertyAPIView(viewsets.ModelViewSet):
    def addtofav(self, request, *args, **kwargs):
        print('herererererer')
        property_id = request.GET.get('property_id')
        user_id = request.GET.get('user_id')
        # property_obj = PropertyNewPage.objects.get(id=property_id)
        if property_id:
            # ser = self.get_serializer(queryset, many=True, context={'language': lang, 'request': request,"locale":locale})
            
            ser = PropertyAddtoFavSerializer(data=request.data,context={'request':request,'property_id':property_id,'user_id':user_id})
            if ser.is_valid():
                ser.save()
                        
                return Response({'result':"success","message":"Property added to favourite"},status.HTTP_200_OK)            
            else:
                errors = { i: ser.errors[i][0] for i in  ser.errors.keys() }
                return Response({"result":"failed","error":errors},status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"result":"failed","error":"Property id cannot be null"},status.HTTP_400_BAD_REQUEST)
    
    
    
class CurrencyChangeAPIView(viewsets.ModelViewSet):
    def currencychange(self,request, *args, **kwargs):
        try:
            # import pdb; pdb.set_trace()
            amount = request.GET.get('amount')
            from_currency = request.GET.get('from_currency')
            to_currency = request.GET.get('to_currency')
            data = {
                'amount': amount,
                'from_currency': from_currency,
                'to_currency': to_currency,
            }
            ser = ChangeCurrencySerializer(data=data, context={'request': request})
            # ser = ChangeCurrencySerializer(data=request,context={'request':request,'amount':amount,'from_currency':from_currency,'to_currency':to_currency}) 
            # import pdb; pdb.set_trace()
            if ser.is_valid():
                obj = ser.save()       
                print(obj)                
                return Response({'result':"success","message":obj},status.HTTP_200_OK) 
            else:
                errors = { i: ser.errors[i][0] for i in  ser.errors.keys() }
                return Response({"result":"failed","error":errors},status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"result":"failed","error":e},status.HTTP_400_BAD_REQUEST)
        
        