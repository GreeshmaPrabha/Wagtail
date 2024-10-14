from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from wagtail.models import Locale
from django.utils.translation import get_language_from_request
from info_page.models import *
from .serializers import *
from django.db.models import Prefetch,Q
from django.db.models import F, Value, IntegerField, FloatField
from django.db.models.functions import Cast
# from .blocks import *
from mysite.constantvariables import PAGINATION_PERPAGE
from django.core.paginator import Paginator
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from wagtail.models import Page


class InformationPagesViewSet(viewsets.ModelViewSet):
    serializer_class = PageSerializer

    #seralizer class for actions
    def get_serializer_class(self):
        # Dictionary to map actions to their respective serializers
        group_serializer = {
            'list': BasePageSerializer,
        }
        
        # Get the appropriate serializer based on the action
        serializer_class = group_serializer.get(self.action, None)
        
        if serializer_class is None:
            raise ValueError(f"No serializer found for action: {self.action}")
        
        return serializer_class


    #lists all infroamtion pages  with pagination
    def list(self, request, *args, **kwargs):
        response = {}
        try:     
            # Get language from the request and fetch corresponding Locale object
            lang = get_language_from_request(request)
            locale = get_object_or_404(Locale, language_code=lang)

            # Get the initial queryset
            parent_page = InformationIndexPage.objects.first()  # Adjust thi
            if parent_page:
                # Return live child pages of the parent EducationPage
                querysets =  Page.objects.child_of(parent_page).specific().select_related('content_type').annotate(model_name=F('content_type__model'))     
            
                # Serialize the paginated records
                serializer = self.get_serializer(querysets, many=True, context={'request': request,'locale':locale})
                
                # Prepare the response data
                response['result'] = 'success'
                response['records'] = serializer.data
            else:
                response['result'] = 'failure'
                response['message'] = 'No models found'
        except Exception as e:
            response['result'] = 'failure'
            response['message'] = str(e)    
        # Return the response with a 200 OK status
        return Response(response, status=status.HTTP_200_OK)
    
    
    def retrieve(self, request, *args, **kwargs):
        response = {}
        try:
            # import pdb; pdb.set_trace()
             # Extract slug from URL parameters
            slug = kwargs.get('slug')
            
            # Get language from the request and fetch corresponding Locale object
            lang = get_language_from_request(request)
            locale = get_object_or_404(Locale, language_code=lang)
            page = Page.objects.get(slug=slug)
            
            if isinstance(page.specific, MultiplePage):
                parent_page = InformationIndexPage.objects.filter(locale=locale).first()
                page_data = Page.objects.live().child_of(parent_page).specific().filter(locale=locale, slug=slug).select_related('content_type').annotate(model_name=F('content_type__model')).first()
                if page_data:
                    sub_pages = Page.objects.live().filter(locale=locale).child_of(page_data).specific().select_related('content_type').annotate(model_name=F('content_type__model'))
                    
                serializer = MultiplePageSerializer(sub_pages,many=True, context={'request': request})
            elif isinstance(page.specific, ContentPage):
                serializer = ContentPageSerializer(page.specific)
            elif isinstance(page.specific, BlogLinkPage):
                serializer = BlogLinkPageSerializer(page.specific)
            else:
                return Response({"error": "Page type not supported."}, status=status.HTTP_400_BAD_REQUEST)            
            
            if serializer and serializer.data is not None:                
                # Prepare the response data
                response['result'] = 'success'
                response['records'] = serializer.data
            else:
                response['result'] = 'failure'   
                response['message'] = 'No data available'
        except Exception as e:
            response['result'] = 'failure'
            response['message'] = str(e)
        # Return the response with a 200 OK status
        return Response(response, status=status.HTTP_200_OK)