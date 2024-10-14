from rest_framework import serializers
from info_page.models import MultiplePage, ContentPage, BlogLinkPage
from mysite.blockserializers import *


class PageSerializer(serializers.Serializer):
    title = serializers.CharField(read_only=True)

class BasePageSerializer(serializers.Serializer):
    title = serializers.CharField(read_only=True)
    slug = serializers.CharField(read_only=True)
    
class InfoPageSerializer(serializers.Serializer):
    title = serializers.CharField(read_only=True)
    slug = serializers.CharField(read_only=True)

class MultiplePageSerializer(InfoPageSerializer, PageContentMixin):
    banner_fields = BannerFieldsSerializer(source='*')  # Include all banner fields
    content = serializers.SerializerMethodField(read_only=True)
    seo_fields = SEOFieldsSerializer(source='*')  # Include all SEO fields
    
    def get_content(self, obj):
        return super().get_content(obj)

class ContentPageSerializer(InfoPageSerializer, PageContentMixin):
    banner_fields = BannerFieldsSerializer(source='*')  # Include all banner fields
    content = serializers.SerializerMethodField(read_only=True)
    seo_fields = SEOFieldsSerializer(source='*')  # Include all SEO fields
    
    def get_content(self, obj):
        return super().get_content(obj)

class BlogLinkPageSerializer(InfoPageSerializer, PageContentMixin):
    banner_fields = BannerFieldsSerializer(source='*')  # Include all banner fields
    content = serializers.SerializerMethodField(read_only=True)
    seo_fields = SEOFieldsSerializer(source='*')  # Include all SEO fields
    
    def get_content(self, obj):
        return super().get_content(obj)
    
