

from rest_framework import serializers
from wagtail.images.api.fields import ImageRenditionField
from wagtail.rich_text import RichText
from wagtail.images.models import Image as WagtailImage
from .models import DeveloperPage
from mysite.utils import get_image_rendition
from bs4 import BeautifulSoup
from django.conf import settings
from mysite.constantvariables import PAGINATION_PERPAGE
from django.core.paginator import Paginator
from django.db import transaction

class DescriptionSerializer(serializers.Serializer):
    description = serializers.CharField()

class DeveloperIconSerializer(serializers.Serializer):
    icon = serializers.SerializerMethodField(read_only=True)
    
    def get_icon(self,obj):
        if obj.get('icon'):
            image = obj.get('icon')
            rendition = get_image_rendition(image, 'original')
            if rendition:
                return {
                    "url": rendition['url'],
                    "full_url": rendition['full_url'],
                    "width": rendition['width'],
                    "height": rendition['height'],
                    "alt": rendition['alt']
                }
        return None 
        

class FaqPointSerializer(serializers.Serializer):
    question = serializers.CharField()
    answer = serializers.CharField()

class FaqSerializer(serializers.Serializer):
    heading = serializers.CharField()
    sub_heading = serializers.CharField()
    points = FaqPointSerializer(many=True)
    
class DeveloperBlockSerializer(serializers.Serializer):
    description = DescriptionSerializer(many=True)
    developer_icon = DeveloperIconSerializer(many=True)
    faq = FaqSerializer()
    
class DeveloperSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    founded_in = serializers.CharField()
    no_of_projects = serializers.CharField()
    price_from = serializers.CharField()
    
class DeveloperDetailBlockSerializer(serializers.Serializer):
    heading = serializers.CharField()
    sub_heading = serializers.CharField()  
    description = serializers.SerializerMethodField()
    
    def get_description(self,obj):
        # import pdb; pdb.set_trace()
        try:
            description = obj.get('description')
            if description:
                return description.source  # Return the HTML content
            return None
        except:
            return None
            
    
class DeveloperPageSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    banner_image = serializers.SerializerMethodField(read_only=True)
    banner_heading = serializers.CharField()
    developer_details = serializers.SerializerMethodField(read_only=True)
    developer_detail_page = serializers.SerializerMethodField(read_only=True)
    developers = serializers.SerializerMethodField(read_only=True)
    
    def get_developers(self,obj):
        if obj:
            dev_detail = obj.developers
            return DeveloperSerializer(dev_detail).data 
    
    def get_banner_image(self, obj):
        if obj.banner_image:
            image = obj.banner_image
            rendition = get_image_rendition(image, 'original')
            if rendition:
                return {
                    "url": rendition['url'],
                    "full_url": rendition['full_url'],
                    "width": rendition['width'],
                    "height": rendition['height'],
                    "alt": rendition['alt']
                }
        return None  
    
    def get_developer_details(self, obj):
        content_blocks = []
        request = self.context.get('request')
        for block in obj.developer_details:
            # print("------block.block_type------",block.block_type)
            if block.block_type == 'developer_detail':
                content_blocks.append({
                    'type': 'developer_detail',
                    'value': DeveloperBlockSerializer(block.value, context={'parent': self}).data
                })
                
                return content_blocks
            
            
    def get_developer_detail_page(self, obj):
        content_blocks = []
        request = self.context.get('request')
        for block in obj.developer_detail_page:
            # print("------block.block_type------",block.block_type)
            if block.block_type == 'detail_content':
                content_blocks.append({
                    'type': 'detail_content',
                    'value': DeveloperDetailBlockSerializer(block.value, context={'parent': self}).data
                })
                
                return content_blocks
        
        
    
    class Meta:
        model = DeveloperPage
        fields = ['id','banner_image','banner_heading','developer_details','developer_detail_page','developers']