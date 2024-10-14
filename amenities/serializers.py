from rest_framework import serializers
from wagtail.images.api.fields import ImageRenditionField
from wagtail.rich_text import RichText
from wagtail.images.models import Image as WagtailImage
from property_new.models import PropertyNewPage, PropertyNewIndexPage,FavouriteProperty
from mysite.utils import get_image_rendition
from bs4 import BeautifulSoup
from django.conf import settings
from mysite.constantvariables import PAGINATION_PERPAGE
from django.core.paginator import Paginator
from django.db import transaction
from mysite.constantvariables import convert_to_choices,CURRENCY_RATES

class AmenitiesBlockSerializer(serializers.Serializer):
    data = serializers.SerializerMethodField() 
    
    def get_data(self,obj):
        try:
            amenity_media = obj.get('facilities_amenities',[])
            formatted_media = []
            
            for media_item in amenity_media:
                icon = media_item.get('icon')
                title = media_item.get('title')
                rendition = get_image_rendition(icon, 'original')
                if rendition:
                    formatted_media.append({
                        "url": rendition['url'],
                        "full_url": rendition['full_url'],
                        "width": rendition['width'],
                        "height": rendition['height'],
                        "alt": rendition['alt'],
                        "title" : title
                    })
            return formatted_media
        
            
        except:
            return None
    
    
class AmenitiesPageSerializer(serializers.Serializer):
    heading = serializers.CharField()
    amenities = serializers.SerializerMethodField()
    
    def get_amenities(self,obj):
        return [
            {
                'type': block.block_type,
                'value': self.serialize_block(block)
            }
            for block in obj.facilities
        ]
        
    def serialize_block(self, block):
        BLOCK_SERIALIZER_MAP = {
            'amenities_facilities': AmenitiesBlockSerializer,
            
        }
        serializer_class = BLOCK_SERIALIZER_MAP.get(block.block_type)
        if serializer_class:
            return serializer_class(block.value, context=self.context).data
       
        return block.block.get_api_representation(block.value, self.context['request'])
    
    